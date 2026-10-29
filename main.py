
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CollegeNetworkDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Cost-Optimized College Network Designer")
        self.root.geometry("1180x780")
        self.root.minsize(950, 650)

        self.nodes = []
        self.edges = []
        self.sorted_edges = []
        self.accepted = []
        self.rejected = []
        self.statuses = []
        self.step_index = 0
        self.current_edge = None
        self.total_cost = 0
        self.finished = True

        self.build_ui()
        self.load_sample()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="Cost-Optimized College Network Designer",
            font=("Segoe UI", 17, "bold")
        )
        title.pack(pady=(10, 3))

        ttk.Label(
            self.root,
            text="Kruskal's Algorithm | Minimum Spanning Tree",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 8))

        main = ttk.Frame(self.root, padding=8)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main, width=310)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        # Building input
        buildings = ttk.LabelFrame(left, text="1. College Buildings", padding=8)
        buildings.pack(fill="x", pady=4)

        self.building_entry = ttk.Entry(buildings)
        self.building_entry.pack(fill="x", pady=4)
        self.building_entry.insert(0, "New Building")

        ttk.Button(
            buildings, text="Add Building", command=self.add_building
        ).pack(fill="x")

        self.building_list = tk.Listbox(buildings, height=5)
        self.building_list.pack(fill="x", pady=(6, 0))

        # Connection input
        connections = ttk.LabelFrame(
            left, text="2. Possible Network Connections", padding=8
        )
        connections.pack(fill="x", pady=4)

        ttk.Label(connections, text="From building").pack(anchor="w")
        self.from_box = ttk.Combobox(connections, state="readonly")
        self.from_box.pack(fill="x", pady=(0, 5))

        ttk.Label(connections, text="To building").pack(anchor="w")
        self.to_box = ttk.Combobox(connections, state="readonly")
        self.to_box.pack(fill="x", pady=(0, 5))

        ttk.Label(connections, text="Installation cost (₹)").pack(anchor="w")
        self.cost_entry = ttk.Entry(connections)
        self.cost_entry.pack(fill="x", pady=(0, 5))

        ttk.Button(
            connections, text="Add Connection", command=self.add_edge
        ).pack(fill="x")

        self.edge_list = ttk.Treeview(
            connections,
            columns=("from", "to", "cost"),
            show="headings",
            height=5
        )
        for col, label in [
            ("from", "From"), ("to", "To"), ("cost", "Cost ₹")
        ]:
            self.edge_list.heading(col, text=label)
            self.edge_list.column(col, width=80, anchor="center")
        self.edge_list.pack(fill="x", pady=6)

        ttk.Button(
            connections, text="Remove Selected Connection",
            command=self.remove_edge
        ).pack(fill="x")

        # Algorithm controls
        controls = ttk.LabelFrame(left, text="3. Run Algorithm", padding=8)
        controls.pack(fill="x", pady=4)

        ttk.Button(
            controls, text="Start / Reset Algorithm",
            command=self.start_algorithm
        ).pack(fill="x", pady=2)

        ttk.Button(
            controls, text="Next Step",
            command=self.next_step
        ).pack(fill="x", pady=2)

        ttk.Button(
            controls, text="Run All Steps",
            command=self.run_all
        ).pack(fill="x", pady=2)

        ttk.Button(
            controls, text="Load Sample Network",
            command=self.load_sample
        ).pack(fill="x", pady=2)

        ttk.Button(
            controls, text="Save Cost Report",
            command=self.save_report
        ).pack(fill="x", pady=2)

        ttk.Label(
            left,
            text="Green = selected\nRed dashed = rejected\nGrey = not yet processed",
            justify="left"
        ).pack(anchor="w", padx=8, pady=8)

        # Graph area
        graph_frame = ttk.LabelFrame(
            right, text="Network Graph", padding=5
        )
        graph_frame.pack(fill="both", expand=True)

        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Status and report area
        self.status_label = ttk.Label(
            right, text="Load a network to begin.", wraplength=780,
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(fill="x", pady=6)

        self.report_text = tk.Text(right, height=7, wrap="word")
        self.report_text.pack(fill="x", pady=(0, 4))
        self.report_text.configure(state="disabled")

    def add_building(self):
        name = self.building_entry.get().strip()

        if not name:
            messagebox.showerror("Invalid input", "Enter a building name.")
            return

        if name in self.nodes:
            messagebox.showerror(
                "Duplicate building", "That building already exists."
            )
            return

        self.nodes.append(name)
        self.building_entry.delete(0, "end")
        self.refresh_inputs()
        self.reset_results()
        self.draw_graph()
        self.update_report("Building added: " + name)

    def add_edge(self):
        u = self.from_box.get()
        v = self.to_box.get()
        raw_cost = self.cost_entry.get().strip()

        if not u or not v:
            messagebox.showerror(
                "Invalid connection", "Add at least two buildings first."
            )
            return

        if u == v:
            messagebox.showerror(
                "Invalid connection",
                "A building cannot connect to itself."
            )
            return

        try:
            cost = float(raw_cost)
            if not math.isfinite(cost) or cost < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid cost",
                "Enter a finite, non-negative numeric cost."
            )
            return

        # Treat connections as undirected. Avoid duplicate building pairs.
        if any(
            {a, b} == {u, v} for a, b, _ in self.edges
        ):
            messagebox.showerror(
                "Duplicate connection",
                "A connection between these buildings already exists."
            )
            return

        self.edges.append((u, v, cost))
        self.cost_entry.delete(0, "end")
        self.refresh_inputs()
        self.reset_results()
        self.draw_graph()
        self.update_report("Connection added: {} — {} (₹{:g})".format(
            u, v, cost
        ))

    def remove_edge(self):
        selected = self.edge_list.selection()
        if not selected:
            messagebox.showinfo(
                "Select a connection",
                "Select a connection from the table first."
            )
            return

        index = self.edge_list.index(selected[0])
        self.edges.pop(index)
        self.refresh_inputs()
        self.reset_results()
        self.draw_graph()
        self.update_report("Selected connection removed.")

    def refresh_inputs(self):
        self.building_list.delete(0, "end")
        for name in self.nodes:
            self.building_list.insert("end", name)

        self.from_box["values"] = self.nodes
        self.to_box["values"] = self.nodes

        self.edge_list.delete(*self.edge_list.get_children())
        for u, v, cost in self.edges:
            self.edge_list.insert(
                "", "end", values=(u, v, "{:g}".format(cost))
            )

    def load_sample(self):
        self.nodes = [
            "Admin Block", "Library", "Computer Lab", "Hostel", "Auditorium"
        ]

        # Example costs in rupees. Replace them with your own estimates.
        self.edges = [
            ("Admin Block", "Library", 20000),
            ("Admin Block", "Computer Lab", 35000),
            ("Admin Block", "Hostel", 25000),
            ("Library", "Computer Lab", 10000),
            ("Library", "Hostel", 30000),
            ("Library", "Auditorium", 18000),
            ("Computer Lab", "Auditorium", 12000),
            ("Hostel", "Auditorium", 22000),
        ]

        self.refresh_inputs()
        self.reset_results()
        self.draw_graph()
        self.update_report(
            "Sample network loaded. Click Start / Reset Algorithm."
        )

    def reset_results(self):
        self.sorted_edges = []
        self.accepted = []
        self.rejected = []
        self.statuses = []
        self.step_index = 0
        self.current_edge = None
        self.total_cost = 0
        self.finished = True
        self.status_label.config(text="Ready. Start the algorithm.")
        self.draw_graph()

    def start_algorithm(self):
        if not self.nodes:
            messagebox.showerror(
                "No buildings", "Add at least one building."
            )
            return

        self.sorted_edges = sorted(
            self.edges, key=lambda e: (e[2], e[0], e[1])
        )
        self.accepted = []
        self.rejected = []
        self.statuses = ["Pending"] * len(self.sorted_edges)
        self.step_index = 0
        self.current_edge = None
        self.total_cost = 0
        self.finished = False

        self.update_report(
            "Algorithm started. Edges are sorted by increasing cost."
        )
        self.draw_graph()

        if len(self.nodes) == 1:
            self.finished = True
            self.status_label.config(
                text="One building: no cable is needed. Minimum cost = ₹0."
            )
            self.update_report(
                "Result: one building, zero connections, total cost ₹0."
            )
        elif not self.sorted_edges:
            self.finished = True
            self.status_label.config(
                text="No connections available. Network is disconnected."
            )
            self.update_report(
                "Result: no edges available; a spanning tree is impossible."
            )

    def find(self, parent, x):
        # Path compression
        if parent[x] != x:
            parent[x] = self.find(parent, parent[x])
        return parent[x]

    def union(self, parent, rank, a, b):
        root_a = self.find(parent, a)
        root_b = self.find(parent, b)

        if root_a == root_b:
            return False

        # Union by rank
        if rank[root_a] < rank[root_b]:
            parent[root_a] = root_b
        elif rank[root_a] > rank[root_b]:
            parent[root_b] = root_a
        else:
            parent[root_b] = root_a
            rank[root_a] += 1

        return True

    def next_step(self):
        if self.finished:
            messagebox.showinfo(
                "Algorithm",
                "No more steps. Start or reset the algorithm to run again."
            )
            return

        if self.step_index >= len(self.sorted_edges):
            self.finish_algorithm()
            return

        u, v, cost = self.sorted_edges[self.step_index]
        self.current_edge = (u, v, cost)

        # Rebuild DSU from already accepted edges.
        parent = {n: n for n in self.nodes}
        rank = {n: 0 for n in self.nodes}
        for a, b, _ in self.accepted:
            self.union(parent, rank, a, b)

        if self.union(parent, rank, u, v):
            self.accepted.append((u, v, cost))
            self.statuses[self.step_index] = "Accepted"
            self.total_cost += cost
            decision = (
                "ACCEPTED: {} — {} (₹{:g}); no cycle is formed."
            ).format(u, v, cost)
        else:
            self.rejected.append((u, v, cost))
            self.statuses[self.step_index] = "Rejected"
            decision = (
                "REJECTED: {} — {} (₹{:g}); it would form a cycle."
            ).format(u, v, cost)

        self.step_index += 1
        self.status_label.config(
            text="Step {} of {}: {}".format(
                self.step_index, len(self.sorted_edges), decision
            )
        )
        self.update_report(decision)
        self.draw_graph()

        if len(self.accepted) == len(self.nodes) - 1:
            self.finish_algorithm()
        elif self.step_index == len(self.sorted_edges):
            self.finish_algorithm()

    def run_all(self):
        if self.finished:
            self.start_algorithm()

        while not self.finished:
            self.next_step()

    def finish_algorithm(self):
        self.finished = True
        connected = len(self.accepted) == len(self.nodes) - 1

        if connected:
            message = (
                "MST complete! Minimum total cost: ₹{:,.2f}. "
                "Selected {} connections."
            ).format(self.total_cost, len(self.accepted))
        else:
            message = (
                "Network is disconnected. Minimum spanning forest cost: "
                "₹{:,.2f}. Only {} of {} buildings are connected in "
                "the selected forest."
            ).format(
                self.total_cost,
                len(self.accepted),
                len(self.nodes)
            )

        self.status_label.config(text=message)
        self.update_report("FINAL RESULT: " + message)
        self.draw_graph()

    def draw_graph(self):
        self.ax.clear()
        self.ax.set_title("College Network: Possible and Selected Links")
        self.ax.axis("off")

        if not self.nodes:
            self.ax.text(
                0.5, 0.5, "Add buildings to display the network",
                ha="center", va="center", transform=self.ax.transAxes
            )
            self.canvas.draw_idle()
            return

        count = len(self.nodes)
        positions = {}

        # Place buildings around a circle.
        for i, node in enumerate(self.nodes):
            angle = 2 * math.pi * i / count + math.pi / 2
            positions[node] = (
                math.cos(angle), math.sin(angle)
            )

        # Draw every possible connection.
        for u, v, cost in self.edges:
            status = "Pending"
            if (u, v, cost) in self.accepted or (
                v, u, cost
            ) in self.accepted:
                status = "Accepted"
            elif (u, v, cost) in self.rejected or (
                v, u, cost
            ) in self.rejected:
                status = "Rejected"

            is_current = self.current_edge == (u, v, cost)

            if status == "Accepted":
                color, style, width = "green", "-", 3
            elif status == "Rejected":
                color, style, width = "red", "--", 1.5
            else:
                color, style, width = "gray", "-", 1

            if is_current:
                color, width = "orange", 3

            x1, y1 = positions[u]
            x2, y2 = positions[v]

            self.ax.plot(
                [x1, x2], [y1, y2],
                color=color, linestyle=style, linewidth=width, zorder=1
            )

            # Offset labels to reduce overlap.
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            length = math.hypot(dx, dy) or 1
            offset = 0.06
            mx -= dy / length * offset
            my += dx / length * offset

            self.ax.text(
                mx, my, "₹{:g}".format(cost),
                fontsize=8, ha="center", va="center",
                bbox=dict(facecolor="white", alpha=0.85, edgecolor="none"),
                zorder=3
            )

        # Draw buildings on top of edges.
        for node, (x, y) in positions.items():
            self.ax.scatter(
                [x], [y], s=1000, color="#dbeafe",
                edgecolors="#2563eb", linewidths=1.5, zorder=4
            )
            self.ax.text(
                x, y, node, fontsize=8, ha="center", va="center",
                zorder=5, wrap=True
            )

        self.ax.text(
            0.02, 0.02,
            "Selected cost: ₹{:,.2f} | Links selected: {}".format(
                self.total_cost, len(self.accepted)
            ),
            transform=self.ax.transAxes, fontsize=9
        )

        self.ax.set_xlim(-1.45, 1.45)
        self.ax.set_ylim(-1.35, 1.35)
        self.figure.tight_layout()
        self.canvas.draw_idle()

    def update_report(self, line):
        self.report_text.configure(state="normal")
        self.report_text.insert("end", line + "\n")
        self.report_text.see("end")
        self.report_text.configure(state="disabled")

    def save_report(self):
        connected = (
            len(self.nodes) > 0
            and len(self.accepted) == len(self.nodes) - 1
        )

        lines = [
            "COST-OPTIMIZED COLLEGE NETWORK DESIGNER",
            "Algorithm: Kruskal's Minimum Spanning Tree",
            "",
            "Buildings: " + ", ".join(self.nodes),
            "",
            "Possible connections:"
        ]

        for u, v, cost in self.edges:
            lines.append("{} -- {} : ₹{:,.2f}".format(u, v, cost))

        lines.extend(["", "Selected connections:"])
        for u, v, cost in self.accepted:
            lines.append("{} -- {} : ₹{:,.2f}".format(u, v, cost))

        lines.extend([
            "",
            "Total selected cost: ₹{:,.2f}".format(self.total_cost),
            "Selected connections: {}".format(len(self.accepted)),
            "All buildings connected: {}".format(
                "Yes" if connected else "No"
            ),
            "Status: {}".format(
                "Minimum spanning tree"
                if connected else "Minimum spanning forest / incomplete"
            ),
            "",
            "Time complexity: O(E log E)",
            "Space complexity: O(V + E)",
            "Note: Costs are illustrative estimates, not vendor quotations."
        ])

        path = filedialog.asksaveasfilename(
            title="Save Cost Report",
            defaultextension=".txt",
            filetypes=[("Text report", "*.txt")]
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write("\n".join(lines))
                messagebox.showinfo(
                    "Report saved", "Report saved successfully:\n" + path
                )
            except OSError as exc:
                messagebox.showerror("Save failed", str(exc))


if __name__ == "__main__":
    root = tk.Tk()
    app = CollegeNetworkDesigner(root)
    root.mainloop()
