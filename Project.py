import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import csv
from datetime import datetime


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker - Smart Personal Expense & Budget Tracker")
        self.root.geometry("1100x670")
        self.root.minsize(980, 620)
        self.root.configure(bg="#F1F5F9")

        # Application State
        self.monthly_budgets = {
            "September 2026": 20000.0,
            "October 2026": 22000.0,
            "November 2026": 25000.0,
            "December 2026": 30000.0,
        }
        self.transactions = []
        self.transaction_counter = 1

        # Configure ttk Styling
        self._setup_styles()

        # Build UI Sections
        self._create_header()
        self._create_main_layout()
        self._load_sample_data()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Treeview Styling
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#1E293B",
            rowheight=30,
            fieldbackground="#FFFFFF",
            font=("Helvetica", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground="#0F172A",
            font=("Helvetica", 10, "bold"),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", "#CBD5E1")], foreground=[("selected", "#0F172A")])

        # Progressbar Styling
        style.configure(
            "Budget.Horizontal.TProgressbar",
            troughcolor="#E2E8F0",
            background="#2563EB",
            thickness=20,
        )

    def _create_header(self):
        header_frame = tk.Frame(self.root, bg="#1E293B", height=60, padx=20)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(
            header_frame,
            text="Finance Tracker",
            font=("Helvetica", 16, "bold"),
            bg="#1E293B",
            fg="#F8FAFC",
        )
        title_lbl.pack(side=tk.LEFT, pady=15)

        subtitle_lbl = tk.Label(
            header_frame,
            text="Personal Expense & Budget Manager",
            font=("Helvetica", 10),
            bg="#1E293B",
            fg="#94A3B8",
        )
        subtitle_lbl.pack(side=tk.LEFT, padx=(12, 0), pady=18)

        # Interactive Month Selector on Right
        month_frame = tk.Frame(header_frame, bg="#1E293B")
        month_frame.pack(side=tk.RIGHT, pady=15)

        tk.Label(
            month_frame,
            text="Billing Cycle:",
            font=("Helvetica", 10),
            bg="#1E293B",
            fg="#CBD5E1",
        ).pack(side=tk.LEFT, padx=(0, 8))

        self.month_var = tk.StringVar(value="November 2026")
        months = list(self.monthly_budgets.keys())
        self.month_combo = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            values=months,
            state="readonly",
            width=16,
            font=("Helvetica", 10),
        )
        self.month_combo.pack(side=tk.LEFT)
        self.month_combo.bind("<<ComboboxSelected>>", self.on_billing_cycle_changed)

    def _create_main_layout(self):
        main_container = tk.Frame(self.root, bg="#F1F5F9", padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        main_container.columnconfigure(0, weight=1, minsize=340)
        main_container.columnconfigure(1, weight=2, minsize=560)
        main_container.rowconfigure(0, weight=1)

        # ================= LEFT PANEL =================
        left_panel = tk.Frame(main_container, bg="#F1F5F9")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # 1. Summary Cards
        summary_frame = tk.LabelFrame(
            left_panel,
            text=" Financial Overview ",
            font=("Helvetica", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=15,
            pady=12,
            relief="groove",
            bd=1,
        )
        summary_frame.pack(fill=tk.X, pady=(0, 15))

        self.balance_var = tk.StringVar(value="₹ 0.00")
        self.income_var = tk.StringVar(value="₹ 0.00")
        self.expense_var = tk.StringVar(value="₹ 0.00")

        self._create_summary_row(summary_frame, "Total Balance:", self.balance_var, "#0F172A")
        self._create_summary_row(summary_frame, "Total Income:", self.income_var, "#10B981")
        self._create_summary_row(summary_frame, "Total Expense:", self.expense_var, "#EF4444")

        # 2. Add Transaction Form
        form_frame = tk.LabelFrame(
            left_panel,
            text=" Add New Transaction ",
            font=("Helvetica", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=15,
            pady=15,
            relief="groove",
            bd=1,
        )
        form_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            form_frame, text="Description:", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#334155"
        ).pack(anchor="w", pady=(0, 4))
        self.desc_entry = tk.Entry(form_frame, font=("Helvetica", 11), relief="solid", bd=1)
        self.desc_entry.pack(fill=tk.X, ipady=5, pady=(0, 12))

        tk.Label(
            form_frame, text="Amount (₹):", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#334155"
        ).pack(anchor="w", pady=(0, 4))
        self.amount_entry = tk.Entry(form_frame, font=("Helvetica", 11), relief="solid", bd=1)
        self.amount_entry.pack(fill=tk.X, ipady=5, pady=(0, 12))

        tk.Label(
            form_frame, text="Category:", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#334155"
        ).pack(anchor="w", pady=(0, 4))
        self.category_var = tk.StringVar(value="Food & Dining")
        categories = [
            "Food & Dining",
            "Transport",
            "Rent & Housing",
            "Utilities & Bills",
            "Shopping",
            "Entertainment",
            "Salary / Freelance",
            "Other",
        ]
        self.category_combo = ttk.Combobox(
            form_frame,
            textvariable=self.category_var,
            values=categories,
            state="readonly",
            font=("Helvetica", 10),
        )
        self.category_combo.pack(fill=tk.X, ipady=4, pady=(0, 12))

        tk.Label(
            form_frame, text="Transaction Type:", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#334155"
        ).pack(anchor="w", pady=(0, 4))

        radio_frame = tk.Frame(form_frame, bg="#FFFFFF")
        radio_frame.pack(fill=tk.X, pady=(0, 18))

        self.type_var = tk.StringVar(value="Expense")
        tk.Radiobutton(
            radio_frame,
            text="Expense (-)",
            variable=self.type_var,
            value="Expense",
            font=("Helvetica", 10),
            bg="#FFFFFF",
            fg="#EF4444",
            selectcolor="#FFFFFF",
            activebackground="#FFFFFF",
        ).pack(side=tk.LEFT, padx=(0, 20))

        tk.Radiobutton(
            radio_frame,
            text="Income (+)",
            variable=self.type_var,
            value="Income",
            font=("Helvetica", 10),
            bg="#FFFFFF",
            fg="#10B981",
            selectcolor="#FFFFFF",
            activebackground="#FFFFFF",
        ).pack(side=tk.LEFT)

        btn_frame = tk.Frame(form_frame, bg="#FFFFFF")
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)

        add_btn = tk.Button(
            btn_frame,
            text="+ Add Transaction",
            command=self.add_transaction,
            font=("Helvetica", 10, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            pady=8,
        )
        add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_fields,
            font=("Helvetica", 10),
            bg="#E2E8F0",
            fg="#334155",
            activebackground="#CBD5E1",
            relief="flat",
            cursor="hand2",
            pady=8,
            padx=15,
        )
        clear_btn.pack(side=tk.RIGHT)

        # ================= RIGHT PANEL =================
        right_panel = tk.Frame(main_container, bg="#F1F5F9")
        right_panel.grid(row=0, column=1, sticky="nsew")

        # 1. Monthly Budget Progress Bar with Set Budget Button
        self.budget_frame = tk.LabelFrame(
            right_panel,
            text=" Monthly Expense Budget Limit ",
            font=("Helvetica", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=15,
            pady=12,
            relief="groove",
            bd=1,
        )
        self.budget_frame.pack(fill=tk.X, pady=(0, 15))

        budget_top_row = tk.Frame(self.budget_frame, bg="#FFFFFF")
        budget_top_row.pack(fill=tk.X, pady=(0, 6))

        self.budget_title_lbl = tk.Label(
            budget_top_row,
            text="",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
        )
        self.budget_title_lbl.pack(side=tk.LEFT)

        edit_budget_btn = tk.Button(
            budget_top_row,
            text="⚙️ Edit Budget",
            command=self.prompt_edit_budget,
            font=("Helvetica", 9, "bold"),
            bg="#F1F5F9",
            fg="#2563EB",
            activebackground="#E2E8F0",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=2,
        )
        edit_budget_btn.pack(side=tk.RIGHT)

        self.progress_bar = ttk.Progressbar(
            self.budget_frame,
            orient="horizontal",
            mode="determinate",
            style="Budget.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(fill=tk.X, pady=(2, 8))

        budget_info_frame = tk.Frame(self.budget_frame, bg="#FFFFFF")
        budget_info_frame.pack(fill=tk.X)

        self.budget_pct_lbl = tk.Label(
            budget_info_frame,
            text="0% of Monthly Budget Used",
            font=("Helvetica", 10, "bold"),
            bg="#FFFFFF",
            fg="#334155",
        )
        self.budget_pct_lbl.pack(side=tk.LEFT)

        self.budget_rem_lbl = tk.Label(
            budget_info_frame,
            text="",
            font=("Helvetica", 10),
            bg="#FFFFFF",
            fg="#64748B",
        )
        self.budget_rem_lbl.pack(side=tk.RIGHT)

        # 2. Transaction History Table
        table_container = tk.LabelFrame(
            right_panel,
            text=" Transaction Ledger ",
            font=("Helvetica", 11, "bold"),
            bg="#FFFFFF",
            fg="#1E293B",
            padx=15,
            pady=12,
            relief="groove",
            bd=1,
        )
        table_container.pack(fill=tk.BOTH, expand=True)

        tree_frame = tk.Frame(table_container, bg="#FFFFFF")
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "date", "desc", "category", "type", "amount")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("desc", text="Description")
        self.tree.heading("category", text="Category")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Amount (₹)")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("date", width=95, anchor="center")
        self.tree.column("desc", width=180, anchor="w")
        self.tree.column("category", width=130, anchor="w")
        self.tree.column("type", width=80, anchor="center")
        self.tree.column("amount", width=110, anchor="e")

        self.tree.tag_configure("Income", foreground="#059669")
        self.tree.tag_configure("Expense", foreground="#DC2626")

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 3. Bottom Table Action Bar
        action_bar = tk.Frame(table_container, bg="#FFFFFF", pady=8)
        action_bar.pack(fill=tk.X, side=tk.BOTTOM)

        del_btn = tk.Button(
            action_bar,
            text="Delete Selected",
            command=self.delete_selected,
            font=("Helvetica", 10),
            bg="#FEE2E2",
            fg="#B91C1C",
            activebackground="#FECACA",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
        )
        del_btn.pack(side=tk.LEFT)

        export_btn = tk.Button(
            action_bar,
            text="Export to CSV",
            command=self.export_csv,
            font=("Helvetica", 10, "bold"),
            bg="#0F172A",
            fg="#FFFFFF",
            activebackground="#334155",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=6,
        )
        export_btn.pack(side=tk.RIGHT)

    def _create_summary_row(self, parent, label_text, text_var, color):
        row = tk.Frame(parent, bg="#FFFFFF")
        row.pack(fill=tk.X, pady=4)
        tk.Label(row, text=label_text, font=("Helvetica", 10), bg="#FFFFFF", fg="#475569").pack(side=tk.LEFT)
        tk.Label(row, textvariable=text_var, font=("Helvetica", 13, "bold"), bg="#FFFFFF", fg=color).pack(
            side=tk.RIGHT
        )

    def prompt_edit_budget(self):
        current_month = self.month_var.get()
        current_budget = self.monthly_budgets.get(current_month, 25000.0)

        new_budget = simpledialog.askfloat(
            "Set Monthly Budget",
            f"Enter new expense budget limit for {current_month} (₹):",
            initialvalue=current_budget,
            minvalue=0.0,
        )

        if new_budget is not None:
            self.monthly_budgets[current_month] = new_budget
            self.refresh_ui()
            messagebox.showinfo("Budget Updated", f"Monthly budget for {current_month} updated to ₹ {new_budget:,.2f}")

    def on_billing_cycle_changed(self, event):
        self.refresh_ui()

    def add_transaction(self):
        desc = self.desc_entry.get().strip()
        amt_str = self.amount_entry.get().strip()
        category = self.category_var.get()
        t_type = self.type_var.get()
        current_cycle = self.month_var.get()

        if not desc:
            messagebox.showwarning("Input Error", "Please enter a transaction description.")
            return

        try:
            amount = float(amt_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid positive number for the amount.")
            return

        record = {
            "id": f"{self.transaction_counter:02d}",
            "billing_cycle": current_cycle,
            "date": datetime.now().strftime("%b %d, %Y"),
            "desc": desc,
            "category": category,
            "type": t_type,
            "amount": amount,
        }
        self.transactions.append(record)
        self.transaction_counter += 1

        self.refresh_ui()
        self.clear_fields()

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a transaction from the table to delete.")
            return

        item_values = self.tree.item(selected[0], "values")
        record_id = item_values[0]

        self.transactions = [t for t in self.transactions if t["id"] != record_id]
        self.refresh_ui()

    def clear_fields(self):
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_var.set("Food & Dining")
        self.type_var.set("Expense")
        self.desc_entry.focus()

    def refresh_ui(self):
        current_cycle = self.month_var.get()
        current_budget = self.monthly_budgets.get(current_cycle, 25000.0)

        # Update Budget Frame Title
        self.budget_title_lbl.config(text=f"Limit: ₹ {current_budget:,.2f} ({current_cycle})")

        # Clear Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        total_income = 0.0
        total_expense = 0.0

        # Filter transactions for the currently selected billing cycle
        cycle_transactions = [t for t in self.transactions if t.get("billing_cycle") == current_cycle]

        for t in cycle_transactions:
            if t["type"] == "Income":
                total_income += t["amount"]
                formatted_amt = f"+ ₹ {t['amount']:,.2f}"
            else:
                total_expense += t["amount"]
                formatted_amt = f"- ₹ {t['amount']:,.2f}"

            self.tree.insert(
                "",
                tk.END,
                values=(t["id"], t["date"], t["desc"], t["category"], t["type"], formatted_amt),
                tags=(t["type"],),
            )

        balance = total_income - total_expense

        # Update Summary Cards
        self.balance_var.set(f"₹ {balance:,.2f}")
        self.income_var.set(f"₹ {total_income:,.2f}")
        self.expense_var.set(f"₹ {total_expense:,.2f}")

        # Update Budget Progress Bar
        pct_used = min((total_expense / current_budget) * 100, 100) if current_budget > 0 else 0
        remaining = current_budget - total_expense

        self.progress_bar["value"] = pct_used
        self.budget_pct_lbl.config(text=f"{pct_used:.1f}% of Monthly Budget Used")

        if remaining >= 0:
            self.budget_rem_lbl.config(text=f"Remaining: ₹ {remaining:,.2f}", fg="#64748B")
        else:
            self.budget_rem_lbl.config(text=f"Over Budget by: ₹ {abs(remaining):,.2f}", fg="#DC2626")

    def export_csv(self):
        current_cycle = self.month_var.get()
        cycle_transactions = [t for t in self.transactions if t.get("billing_cycle") == current_cycle]

        if not cycle_transactions:
            messagebox.showinfo("Export Empty", f"There are no transactions in {current_cycle} to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=f"FinTrack_{current_cycle.replace(' ', '_')}.csv",
        )
        if not file_path:
            return

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Billing Cycle", "Date", "Description", "Category", "Type", "Amount"])
                for t in cycle_transactions:
                    writer.writerow([t["id"], t["billing_cycle"], t["date"], t["desc"], t["category"], t["type"], t["amount"]])
            messagebox.showinfo("Export Successful", f"Transactions saved successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export CSV:\n{e}")

    def _load_sample_data(self):
        samples = [
            ("November 2026", "Monthly Salary", 60000.0, "Salary / Freelance", "Income"),
            ("November 2026", "Apartment Rent", 12500.0, "Rent & Housing", "Expense"),
            ("November 2026", "Supermarket Groceries", 3200.0, "Food & Dining", "Expense"),
            ("November 2026", "Metro & Cab Commute", 1800.0, "Transport", "Expense"),
            ("October 2026", "October Freelance", 15000.0, "Salary / Freelance", "Income"),
            ("October 2026", "Electricity Bill", 2400.0, "Utilities & Bills", "Expense"),
        ]
        for cycle, desc, amt, cat, t_type in samples:
            self.transactions.append(
                {
                    "id": f"{self.transaction_counter:02d}",
                    "billing_cycle": cycle,
                    "date": datetime.now().strftime("%b %d, %Y"),
                    "desc": desc,
                    "category": cat,
                    "type": t_type,
                    "amount": amt,
                }
            )
            self.transaction_counter += 1
        self.refresh_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()