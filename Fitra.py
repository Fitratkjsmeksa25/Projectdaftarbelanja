import tkinter as tk
from tkinter import ttk, messagebox
import penyimpanan

# ==============================
# MY SHOPPING LIST
# ==============================

BG = "#F4F7F5"
GREEN = "#21865A"
DARK_GREEN = "#176B46"
WHITE = "#FFFFFF"
TEXT = "#20332A"
GRAY = "#718078"
RED = "#D9534F"


class ShoppingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("My Shopping List")
        self.root.geometry("760x620")
        self.root.minsize(650, 550)
        self.root.configure(bg=BG)

        self.items = penyimpanan.muat_data()

        self.create_style()
        self.create_widgets()
        self.refresh_list()

    # ==============================
    # STYLE
    # ==============================

    def create_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#E8F1EB",
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCEFE4")]
        )

    # ==============================
    # TAMPILAN UTAMA
    # ==============================

    def create_widgets(self):

        header = tk.Frame(
            self.root,
            bg=GREEN,
            height=125
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🛒 MY SHOPPING LIST",
            font=("Segoe UI", 22, "bold"),
            bg=GREEN,
            fg=WHITE
        ).pack(anchor="w", padx=30, pady=(25, 5))

        tk.Label(
            header,
            text="Catat kebutuhanmu, belanja jadi lebih teratur.",
            font=("Segoe UI", 10),
            bg=GREEN,
            fg=WHITE
        ).pack(anchor="w", padx=32)

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=28, pady=20)

        # KARTU RINGKASAN

        summary = tk.Frame(main, bg=BG)
        summary.pack(fill="x", pady=(0, 18))

        self.total_label = self.create_card(
            summary, "TOTAL BARANG", 0
        )

        self.done_label = self.create_card(
            summary, "SUDAH DIBELI", 1
        )

        self.remaining_label = self.create_card(
            summary, "BELUM DIBELI", 2
        )

        # INPUT BARANG

        input_card = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground="#E4ECE7",
            highlightthickness=1
        )
        input_card.pack(fill="x", pady=(0, 15))

        tk.Label(
            input_card,
            text="Tambah Barang",
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w", padx=18, pady=(15, 8))

        input_row = tk.Frame(input_card, bg=WHITE)
        input_row.pack(fill="x", padx=18, pady=(0, 15))

        self.entry = tk.Entry(
            input_row,
            font=("Segoe UI", 11),
            bg="#F8FAF8",
            fg=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#E4ECE7"
        )
        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=10
        )

        self.entry.bind(
            "<Return>",
            lambda event: self.add_item()
        )

        tk.Button(
            input_row,
            text="+ Tambah",
            command=self.add_item,
            bg=GREEN,
            fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        ).pack(side="left", padx=(10, 0))

        # DAFTAR BARANG

        list_card = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground="#E4ECE7",
            highlightthickness=1
        )
        list_card.pack(fill="both", expand=True)

        top = tk.Frame(list_card, bg=WHITE)
        top.pack(fill="x", padx=18, pady=15)

        tk.Label(
            top,
            text="Daftar Belanja",
            font=("Segoe UI", 12, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(side="left")

        self.search_var = tk.StringVar()

        search = tk.Entry(
            top,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            width=22,
            relief="flat",
            bg="#F4F7F5"
        )
        search.pack(side="right", ipady=7)

        search.bind(
            "<KeyRelease>",
            lambda event: self.refresh_list()
        )

        # TABEL

        table_frame = tk.Frame(list_card, bg=WHITE)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=18
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=("status", "nama"),
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("status", text="STATUS")
        self.tree.heading("nama", text="NAMA BARANG")

        self.tree.column(
            "status",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "nama",
            width=400,
            anchor="w"
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<Double-1>",
            lambda event: self.toggle_item()
        )

        # TOMBOL AKSI

        actions = tk.Frame(list_card, bg=WHITE)
        actions.pack(fill="x", padx=18, pady=15)

        tk.Button(
            actions,
            text="✓ Tandai / Batalkan",
            command=self.toggle_item,
            bg=GREEN,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=9,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            actions,
            text="Hapus Barang",
            command=self.delete_item,
            bg=RED,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=9,
            cursor="hand2"
        ).pack(side="left", padx=8)

        tk.Button(
            actions,
            text="Hapus Semua",
            command=self.clear_all,
            bg="#E8F1EB",
            fg=TEXT,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=9,
            cursor="hand2"
        ).pack(side="right")

        tk.Label(
            main,
            text="Tips: Klik dua kali barang untuk mengubah status.",
            bg=BG,
            fg=GRAY,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(10, 0))

    # ==============================
    # KARTU RINGKASAN
    # ==============================

    def create_card(self, parent, title, column):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground="#E4ECE7",
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=5
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=15, pady=(12, 2))

        label = tk.Label(
            card,
            text="0",
            bg=WHITE,
            fg=GREEN,
            font=("Segoe UI", 22, "bold")
        )

        label.pack(anchor="w", padx=15, pady=(0, 12))

        return label

    # ==============================
    # TAMBAH BARANG
    # ==============================

    def add_item(self):

        name = self.entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Peringatan",
                "Masukkan nama barang terlebih dahulu!"
            )
            return

        self.items.append({
            "name": name,
            "done": False
        })

        self.entry.delete(0, tk.END)

        self.save_data()
        self.refresh_list()

    # ==============================
    # PILIH BARANG
    # ==============================

    def get_selected_index(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showinfo(
                "Informasi",
                "Silakan pilih barang terlebih dahulu."
            )
            return None

        return int(selected[0])

    # ==============================
    # CHECKLIST
    # ==============================

    def toggle_item(self):

        index = self.get_selected_index()

        if index is None:
            return

        self.items[index]["done"] = not self.items[index]["done"]

        self.save_data()
        self.refresh_list()

    # ==============================
    # HAPUS BARANG
    # ==============================

    def delete_item(self):

        index = self.get_selected_index()

        if index is None:
            return

        del self.items[index]

        self.save_data()
        self.refresh_list()

    # ==============================
    # HAPUS SEMUA
    # ==============================

    def clear_all(self):

        if not self.items:
            return

        confirm = messagebox.askyesno(
            "Konfirmasi",
            "Apakah kamu yakin ingin menghapus semua barang?"
        )

        if confirm:
            self.items.clear()
            self.save_data()
            self.refresh_list()

    # ==============================
    # MENAMPILKAN DAFTAR
    # ==============================

    def refresh_list(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        keyword = self.search_var.get().lower()

        for index, item in enumerate(self.items):

            if keyword not in item["name"].lower():
                continue

            if item["done"]:
                status = "✓ Sudah dibeli"
            else:
                status = "○ Belum dibeli"

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(status, item["name"])
            )

        total = len(self.items)

        done = sum(
            1 for item in self.items
            if item["done"]
        )

        remaining = total - done

        self.total_label.config(text=str(total))
        self.done_label.config(text=str(done))
        self.remaining_label.config(text=str(remaining))

    # ==============================
    # SIMPAN DATA
    # ==============================

    def save_data(self):

        if not penyimpanan.simpan_data(self.items):
            messagebox.showerror(
                "Kesalahan",
                "Data gagal disimpan."
            )


# ==============================
# MENJALANKAN APLIKASI
# ==============================

if __name__ == "__main__":

    root = tk.Tk()

    app = ShoppingApp(root)

    root.mainloop()