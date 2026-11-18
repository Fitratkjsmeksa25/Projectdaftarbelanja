import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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


def format_rupiah(angka):
    return "Rp " + f"{angka:,}".replace(",", ".")


class ShoppingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("My Shopping List")
        self.root.geometry("880x660")
        self.root.minsize(780, 580)
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

        self.total_price_label = self.create_card(
            summary, "TOTAL BELANJA", 3, size=15
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

        self.category_box = ttk.Combobox(
            input_row,
            values=penyimpanan.KATEGORI,
            state="readonly",
            width=11,
            font=("Segoe UI", 10)
        )
        self.category_box.set("Lainnya")
        self.category_box.pack(side="left", padx=(10, 0), ipady=8)

        tk.Label(
            input_row,
            text="Jml",
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(10, 4))

        self.qty_entry = tk.Entry(
            input_row,
            width=5,
            font=("Segoe UI", 11),
            bg="#F8FAF8",
            fg=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#E4ECE7"
        )
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", ipady=10)

        self.qty_entry.bind(
            "<Return>",
            lambda event: self.add_item()
        )

        tk.Label(
            input_row,
            text="Harga",
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(10, 4))

        self.price_entry = tk.Entry(
            input_row,
            width=10,
            font=("Segoe UI", 11),
            bg="#F8FAF8",
            fg=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#E4ECE7"
        )
        self.price_entry.pack(side="left", ipady=10)

        self.price_entry.bind(
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
            width=16,
            relief="flat",
            bg="#F4F7F5"
        )
        search.pack(side="right", ipady=7)

        search.bind(
            "<KeyRelease>",
            lambda event: self.refresh_list()
        )

        self.filter_kategori = ttk.Combobox(
            top,
            values=["Semua kategori"] + penyimpanan.KATEGORI,
            state="readonly",
            width=14,
            font=("Segoe UI", 9)
        )
        self.filter_kategori.set("Semua kategori")
        self.filter_kategori.pack(side="right", padx=(0, 8))

        self.filter_kategori.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_list()
        )

        self.filter_status = ttk.Combobox(
            top,
            values=["Semua", "Belum dibeli", "Sudah dibeli"],
            state="readonly",
            width=12,
            font=("Segoe UI", 9)
        )
        self.filter_status.set("Semua")
        self.filter_status.pack(side="right", padx=(0, 8))

        self.filter_status.bind(
            "<<ComboboxSelected>>",
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
            columns=("status", "nama", "kategori", "jumlah", "harga", "subtotal"),
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("status", text="STATUS")
        self.tree.heading("nama", text="NAMA BARANG")
        self.tree.heading("kategori", text="KATEGORI")
        self.tree.heading("jumlah", text="JML")
        self.tree.heading("harga", text="HARGA")
        self.tree.heading("subtotal", text="SUBTOTAL")

        self.tree.column(
            "status",
            width=120,
            anchor="center"
        )

        self.tree.column(
            "nama",
            width=200,
            anchor="w"
        )

        self.tree.column(
            "kategori",
            width=100,
            anchor="center"
        )

        self.tree.column(
            "jumlah",
            width=50,
            anchor="center"
        )

        self.tree.column(
            "harga",
            width=100,
            anchor="e"
        )

        self.tree.column(
            "subtotal",
            width=110,
            anchor="e"
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
            text="Ubah Barang",
            command=self.edit_item,
            bg=DARK_GREEN,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=9,
            cursor="hand2"
        ).pack(side="left", padx=(8, 0))

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

    def create_card(self, parent, title, column, size=22):

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
            font=("Segoe UI", size, "bold")
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

        if self.nama_sudah_ada(name):
            messagebox.showwarning(
                "Peringatan",
                "Barang tersebut sudah ada di daftar!"
            )
            return

        try:
            qty = int(self.qty_entry.get().strip() or "1")
            price = int(self.price_entry.get().strip() or "0")
        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Jumlah dan harga harus berupa angka!"
            )
            return

        if qty < 1 or price < 0:
            messagebox.showwarning(
                "Peringatan",
                "Jumlah minimal 1 dan harga tidak boleh negatif!"
            )
            return

        self.items.append({
            "name": name,
            "category": self.category_box.get(),
            "qty": qty,
            "price": price,
            "done": False
        })

        self.entry.delete(0, tk.END)
        self.qty_entry.delete(0, tk.END)
        self.qty_entry.insert(0, "1")
        self.price_entry.delete(0, tk.END)

        self.save_data()
        self.refresh_list()

    # ==============================
    # CEK DUPLIKAT
    # ==============================

    def nama_sudah_ada(self, name, kecuali=None):

        for index, item in enumerate(self.items):

            if index == kecuali:
                continue

            if item["name"].lower() == name.lower():
                return True

        return False

    # ==============================
    # UBAH BARANG
    # ==============================

    def edit_item(self):

        index = self.get_selected_index()

        if index is None:
            return

        item = self.items[index]

        name = simpledialog.askstring(
            "Ubah Barang",
            "Nama barang:",
            initialvalue=item["name"],
            parent=self.root
        )

        if name is None:
            return

        name = name.strip()

        if not name:
            messagebox.showwarning(
                "Peringatan",
                "Nama barang tidak boleh kosong!"
            )
            return

        if self.nama_sudah_ada(name, kecuali=index):
            messagebox.showwarning(
                "Peringatan",
                "Barang tersebut sudah ada di daftar!"
            )
            return

        qty = simpledialog.askinteger(
            "Ubah Barang",
            "Jumlah:",
            initialvalue=item["qty"],
            minvalue=1,
            parent=self.root
        )

        if qty is None:
            return

        price = simpledialog.askinteger(
            "Ubah Barang",
            "Harga satuan (Rp):",
            initialvalue=item["price"],
            minvalue=0,
            parent=self.root
        )

        if price is None:
            return

        category = simpledialog.askstring(
            "Ubah Barang",
            "Kategori (" + ", ".join(penyimpanan.KATEGORI) + "):",
            initialvalue=item["category"],
            parent=self.root
        )

        if category is None:
            return

        category = category.strip().capitalize()

        if category not in penyimpanan.KATEGORI:
            messagebox.showwarning(
                "Peringatan",
                "Kategori harus salah satu dari: "
                + ", ".join(penyimpanan.KATEGORI)
            )
            return

        item["name"] = name
        item["category"] = category
        item["qty"] = qty
        item["price"] = price

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
        filter_status = self.filter_status.get()
        filter_kategori = self.filter_kategori.get()

        for index, item in enumerate(self.items):

            if keyword not in item["name"].lower():
                continue

            if filter_status == "Belum dibeli" and item["done"]:
                continue

            if filter_status == "Sudah dibeli" and not item["done"]:
                continue

            if (
                filter_kategori != "Semua kategori"
                and item["category"] != filter_kategori
            ):
                continue

            if item["done"]:
                status = "✓ Sudah dibeli"
            else:
                status = "○ Belum dibeli"

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    status,
                    item["name"],
                    item["category"],
                    item["qty"],
                    format_rupiah(item["price"]),
                    format_rupiah(item["qty"] * item["price"])
                )
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

        total_price = sum(
            item["qty"] * item["price"]
            for item in self.items
        )

        self.total_price_label.config(
            text=format_rupiah(total_price)
        )

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