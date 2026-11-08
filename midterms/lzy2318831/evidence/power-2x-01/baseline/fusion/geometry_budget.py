"""Server-lifetime budget shared by fresh geometry matches, never reset by UI."""
import threading
from .live_session import MatchLedger
from .llm import CallFailure,PRICES,MAX_OUTPUT,canonical


class ServerBudget:
    def __init__(self,max_calls=12,budget_usd=.50):
        self.lock=threading.RLock();self.max_calls=max_calls;self.budget_usd=budget_usd
        self.calls=0;self.committed=0.;self.known=0.;self.unknown=0

    def snapshot(self):
        with self.lock:
            return dict(calls=self.calls,call_cap=self.max_calls,
                committed_or_reserved_usd=self.committed,cost_cap_usd=self.budget_usd,
                known_estimated_usd=self.known,unknown_cost_calls=self.unknown,
                can_start=self.max_calls-self.calls>=6 and self.budget_usd-self.committed>=.25-1e-9,
                scope='this server process; new match does not reset cumulative spending')


class GeometryMatchLedger(MatchLedger):
    def __init__(self,path,cancel_event,server_budget):
        super().__init__(path,cancel_event);self.server_budget=server_budget

    def reserve(self,payload,live):
        budget=self.server_budget
        rates=PRICES[payload['model']]
        estimate=((len(canonical(payload))+4096)*rates[0]+MAX_OUTPUT*rates[1])/1e6
        with budget.lock:
            if budget.calls>=budget.max_calls or budget.committed+estimate>budget.budget_usd:
                raise CallFailure('model_call_limit',dict(error_kind='server_budget_exhausted',network_attempted=False,
                    estimated_cost_usd=0,usage=dict(input_tokens=0,output_tokens=0,total_tokens=0)))
            reserve=super().reserve(payload,live)
            budget.calls+=1;budget.committed+=reserve
            return reserve

    def finish(self,reserve,metadata):
        with self.server_budget.lock:
            super().finish(reserve,metadata)
            cost=metadata.get('estimated_cost_usd')
            if cost is None:self.server_budget.unknown+=1
            else:
                self.server_budget.known+=cost;self.server_budget.committed+=cost-reserve
