from ._anvil_designer import MainViewTemplate
from anvil import *
import anvil.server
import anvil.js


class MainView(MainViewTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.dom_nodes["tcp_check_button"].addEventListener("click", self._on_tcp_check_click)
        self.dom_nodes["udp_check_button"].addEventListener("click", self._on_udp_check_click)
        self.dom_nodes["dns_check_button"].addEventListener("click", self._on_dns_check_click)

        self.dom_nodes["tcp_form"].addEventListener("submit", self._on_tcp_form_submit)
        self.dom_nodes["udp_form"].addEventListener("submit", self._on_udp_form_submit)
        self.dom_nodes["dns_form"].addEventListener("submit", self._on_dns_form_submit)

    def _on_tcp_form_submit(self, event):
        event.preventDefault()
        self._on_tcp_check_click(event)

    def _on_udp_form_submit(self, event):
        event.preventDefault()
        self._on_udp_check_click(event)

    def _on_dns_form_submit(self, event):
        event.preventDefault()
        self._on_dns_check_click(event)

    def _read_host_port(self, host_key, port_key):
        host = (self.dom_nodes[host_key].value or "").strip()
        if not host:
            return None, None

        try:
            port = int(self.dom_nodes[port_key].value)
        except (TypeError, ValueError):
            return None, None

        return host, port

    def _set_port_result(self, prefix, host, port, resolved_ip, status):
        self.dom_nodes[f"{prefix}_result_message"].textContent = f"{host}:{port}"
        self.dom_nodes[f"{prefix}_resolved_ip_text"].textContent = resolved_ip or "–"
        self.dom_nodes[f"{prefix}_status_text"].textContent = status or "error"

        anvil.js.window.document.getElementById(f"{prefix}-result-section").hidden = False

    def _set_button_busy(self, btn_key, busy):
        btn = self.dom_nodes[btn_key]
        if busy:
            btn.setAttribute("aria-busy", "true")
            btn.disabled = True
        else:
            btn.removeAttribute("aria-busy")
            btn.disabled = False

    def _on_tcp_check_click(self, event):
        host, port = self._read_host_port("tcp_host_input", "tcp_port_input")
        if not host:
            return

        self._set_button_busy("tcp_check_button", True)

        try:
            res = anvil.server.call_s("check_port", host, port)
        except Exception:
            self._set_port_result("tcp", host, port, None, "error")
        else:
            self._set_port_result(
                "tcp",
                res.get("host") or host,
                res.get("port") or port,
                res.get("resolved_ip"),
                res.get("status"),
            )
        finally:
            self._set_button_busy("tcp_check_button", False)

    def _on_udp_check_click(self, event):
        host, port = self._read_host_port("udp_host_input", "udp_port_input")
        if not host:
            return

        self._set_button_busy("udp_check_button", True)

        try:
            res = anvil.server.call_s("check_udp_port", host, port)
        except Exception:
            self._set_port_result("udp", host, port, None, "error")
        else:
            self._set_port_result(
                "udp",
                res.get("host") or host,
                res.get("port") or port,
                res.get("resolved_ip"),
                res.get("status"),
            )
        finally:
            self._set_button_busy("udp_check_button", False)

    def _on_dns_check_click(self, event):
        target = (self.dom_nodes["dns_target_input"].value or "").strip()
        if not target:
            return

        self._set_button_busy("dns_check_button", True)

        try:
            data = anvil.server.call_s("dns_propagation", target)
        except Exception as e:
            self.dom_nodes["dns_summary_text"].textContent = ""
            self.dom_nodes["dns_error_text"].textContent = str(e)
            self._render_dns_rows([])
        else:
            self.dom_nodes["dns_summary_text"].textContent = f"{data.get('display_target', target)}"
            self.dom_nodes["dns_error_text"].textContent = ""
            self._render_dns_rows(data.get("results", []))
        finally:
            self._set_button_busy("dns_check_button", False)

        anvil.js.window.document.getElementById("dns-result-section").hidden = False

    def _render_dns_rows(self, results):
        doc = anvil.js.window.document
        tbody = self.dom_nodes["dns_results_tbody"]

        while tbody.firstChild:
            tbody.removeChild(tbody.firstChild)

        for r in results:
            tr = doc.createElement("tr")

            ips = r.get("ips") or []
            ip_cell_text = ", ".join(ips) if ips else "–"
            resolver_label = r.get("resolver_name", "Unknown")
            country = r.get("country")
            if country:
                resolver_label = f"{resolver_label} ({country})"

            td_resolver = doc.createElement("td")
            td_resolver.textContent = resolver_label
            tr.appendChild(td_resolver)

            td_ips = doc.createElement("td")
            td_ips.textContent = ip_cell_text
            tr.appendChild(td_ips)

            td_status = doc.createElement("td")
            mark = doc.createElement("mark")
            mark.textContent = r.get("status", "unknown")
            td_status.appendChild(mark)
            tr.appendChild(td_status)

            tbody.appendChild(tr)
