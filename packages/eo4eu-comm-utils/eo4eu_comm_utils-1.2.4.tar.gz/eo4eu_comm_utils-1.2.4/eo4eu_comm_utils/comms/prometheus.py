from enum import Enum
from eo4eu_base_utils import OptionalModule

from .interface import Comm


_prometheus_module = OptionalModule(
    package = "eo4eu_comm_utils",
    enabled_by = ["prometheus", "full"],
    depends_on = ["prometheus_client"]
)

if _prometheus_module.is_enabled():
    from prometheus_client import Counter, Gauge, start_http_server

    class CounterComm(Comm):
        def __init__(self, counter: Counter):
            self._counter = counter

        def send(self, value: int = 1, **kwargs):
            self._counter.inc(value)


    class GaugeComm(Comm):
        def __init__(self, counter: Counter):
            self._counter = counter

        def send(self, value: int = 1, **kwargs):
            self._counter.set(value)


    def _wrap_metric(metric: Counter|Gauge) -> CounterComm|GaugeComm:
        if isinstance(metric, Counter):
            return CounterComm(metric)
        if isinstance(metric, Gauge):
            return GaugeComm(metric)
        raise ValueError(f"PrometheusComm expects either Counter or Gauge, not {metric.__class__.__name__}")


    class PrometheusComm(Comm):
        def __init__(self, input: dict[Enum,Counter|Gauge], port: int = 8000):
            start_http_server(port)
            self._metrics = {
                kind: _wrap_metric(metric)
                for kind, metric in input.items()
            }

        def send(self, *kinds: Enum, value: int = 1, **kwargs):
            for kind in kinds:
                self._metrics[kind].send(value, **kwargs)
else:
    Counter = _prometheus_module.broken_class("Counter")
    Gauge = _prometheus_module.broken_class("Gauge")
    PrometheusComm = _prometheus_module.broken_class("PrometheusComm")
