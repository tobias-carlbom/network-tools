from ._anvil_designer import MainViewTemplate
from anvil import *
import anvil.server
import anvil.js


class MainView(MainViewTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.dom_nodes["port_check_button"].addEventListener(
            "click", self._on_port_check_click
        )
        self.dom_nodes["dns_check_button"].addEventListener(
            "click", self._on_dns_check_click
        )

    def _on_port_check_click(self, event):
        host = (self.dom_nodes["port_host_input"].value or "").strip()
        if not host:
            return

        try:
            port = int(self.dom_nodes["port_port_input"].value)
        except (TypeError, ValueError):
            return

        try:
            res = anvil.server.call("check_port", host, port)
        except Exception as e:
            self.dom_nodes["port_result_message"].textContent = f"{host}:{port}"
            self.dom_nodes["port_resolved_ip_text"].textContent = "–"
            self.dom_nodes["port_status_text"].textContent = "error"
            self.dom_nodes["port_error_text"].textContent = str(e)
        else:
            self.dom_nodes["port_result_message"].textContent = (
                f"{res['host']}:{res['port']}"
            )
            self.dom_nodes["port_resolved_ip_text"].textContent = (
                res["resolved_ip"] or "–"
            )
            self.dom_nodes["port_status_text"].textContent = res["status"]
            #self.dom_nodes["port_error_text"].textContent = res["error"] or "None"

        anvil.js.window.document.getElementById("port-result-section").hidden = False

    def _on_dns_check_click(self, event):
        target = (self.dom_nodes["dns_target_input"].value or "").strip()
        if not target:
            return

        try:
            data = anvil.server.call("dns_a_propagation", target)
        except Exception as e:
            self.dom_nodes["dns_summary_text"].textContent = ""
            self.dom_nodes["dns_error_text"].textContent = str(e)
            self._render_dns_rows([])
        else:
            self.dom_nodes["dns_summary_text"].textContent = (
                f"Results for {data['target']}"
            )
            self.dom_nodes["dns_error_text"].textContent = ""
            self._render_dns_rows(data["results"])

        anvil.js.window.document.getElementById("dns-result-section").hidden = False

    def _render_dns_rows(self, results):
        doc = anvil.js.window.document
        tbody = self.dom_nodes["dns_results_tbody"]

        while tbody.firstChild:
            tbody.removeChild(tbody.firstChild)

        for r in results:
            tr = doc.createElement("tr")

            vals = [
                r["resolver_name"],
                ", ".join(r["ips"]) if r["ips"] else "–",
                str(r["ttl"]) if r["ttl"] is not None else "–",
                r["status"],
            ]

            for v in vals:
                td = doc.createElement("td")
                td.textContent = v
                tr.appendChild(td)

            tbody.appendChild(tr)
