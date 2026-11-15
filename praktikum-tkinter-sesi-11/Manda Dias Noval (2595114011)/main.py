import tkinter as tk
from tkinter import ttk, messagebox


class PendaftaranApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pendaftaran Kegiatan Mahasiswa")
        self.root.geometry("760x680")
        self.root.minsize(680, 600)

        self.nama_var = tk.StringVar()
        self.prodi_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="")
        self.kegiatan_vars = {
            "Seminar Teknologi": tk.BooleanVar(),
            "Workshop Pemrograman": tk.BooleanVar(),
            "Kompetisi IT": tk.BooleanVar(),
            "Organisasi Mahasiswa": tk.BooleanVar(),
        }

        self.create_menu()
        self.create_widgets()
        self.root.bind("<Return>", self.submit)

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Keluar", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Bantuan", menu=help_menu)

        self.root.config(menu=menubar)

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="FORM PENDAFTARAN KEGIATAN MAHASISWA",
            font=("Arial", 15, "bold")
        )
        title.pack(pady=(15, 10))

        form = ttk.LabelFrame(self.root, text="Data Pendaftaran", padding=12)
        form.pack(fill="x", padx=18, pady=8)

        ttk.Label(form, text="Nama Lengkap").grid(row=0, column=0, sticky="w", pady=6)
        self.nama_entry = ttk.Entry(form, textvariable=self.nama_var, width=45)
        self.nama_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=6)

        ttk.Label(form, text="Program Studi").grid(row=1, column=0, sticky="w", pady=6)
        prodi = ttk.Combobox(
            form,
            textvariable=self.prodi_var,
            values=[
                "Teknik Informatika",
                "Sistem Informasi",
                "Teknologi Informasi",
                "Teknik Elektro",
                "Teknik Mesin",
            ],
            state="readonly",
            width=42
        )
        prodi.grid(row=1, column=1, sticky="ew", padx=10, pady=6)

        ttk.Label(form, text="Jenis Kelamin").grid(row=2, column=0, sticky="w", pady=6)
        gender_frame = ttk.Frame(form)
        gender_frame.grid(row=2, column=1, sticky="w", padx=10, pady=6)
        ttk.Radiobutton(
            gender_frame, text="Laki-laki", variable=self.gender_var, value="Laki-laki"
        ).pack(side="left", padx=(0, 15))
        ttk.Radiobutton(
            gender_frame, text="Perempuan", variable=self.gender_var, value="Perempuan"
        ).pack(side="left")

        ttk.Label(form, text="Pilih Kegiatan").grid(row=3, column=0, sticky="nw", pady=6)
        activity_frame = ttk.Frame(form)
        activity_frame.grid(row=3, column=1, sticky="w", padx=10, pady=6)
        for i, (activity, variable) in enumerate(self.kegiatan_vars.items()):
            ttk.Checkbutton(
                activity_frame, text=activity, variable=variable
            ).grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 18), pady=2)

        ttk.Label(form, text="Alasan Mengikuti").grid(row=4, column=0, sticky="nw", pady=6)
        self.alasan_text = tk.Text(form, width=45, height=4, wrap="word")
        self.alasan_text.grid(row=4, column=1, sticky="ew", padx=10, pady=6)

        form.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=18, pady=8)
        ttk.Button(button_frame, text="Submit", command=self.submit).pack(side="left")
        ttk.Button(button_frame, text="Reset", command=self.reset).pack(side="left", padx=8)

        result_frame = ttk.LabelFrame(self.root, text="Ringkasan Pendaftaran", padding=10)
        result_frame.pack(fill="both", expand=True, padx=18, pady=(5, 15))

        self.result_text = tk.Text(result_frame, height=8, wrap="word", state="disabled")
        self.result_text.pack(fill="both", expand=True)

        list_frame = ttk.LabelFrame(self.root, text="Daftar Kegiatan yang Dipilih", padding=8)
        list_frame.pack(fill="x", padx=18, pady=(0, 12))
        self.activity_list = tk.Listbox(list_frame, height=4)
        self.activity_list.pack(fill="x")

        self.nama_entry.focus_set()

    def submit(self, event=None):
        nama = self.nama_var.get().strip()
        if not nama:
            messagebox.showwarning("Validasi", "Nama tidak boleh kosong.")
            self.nama_entry.focus_set()
            return

        prodi = self.prodi_var.get() or "Belum dipilih"
        gender = self.gender_var.get() or "Belum dipilih"
        kegiatan = [
            name for name, variable in self.kegiatan_vars.items() if variable.get()
        ]
        alasan = self.alasan_text.get("1.0", "end").strip() or "Tidak diisi"

        if not kegiatan:
            messagebox.showwarning("Validasi", "Pilih minimal satu kegiatan.")
            return

        ringkasan = (
            f"Nama             : {nama}\n"
            f"Program Studi    : {prodi}\n"
            f"Jenis Kelamin    : {gender}\n"
            f"Kegiatan         : {', '.join(kegiatan)}\n"
            f"Alasan           : {alasan}\n"
        )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", ringkasan)
        self.result_text.config(state="disabled")

        self.activity_list.delete(0, "end")
        for item in kegiatan:
            self.activity_list.insert("end", item)

        messagebox.showinfo("Berhasil", "Pendaftaran berhasil diproses.")

    def reset(self):
        self.nama_var.set("")
        self.prodi_var.set("")
        self.gender_var.set("")
        for variable in self.kegiatan_vars.values():
            variable.set(False)
        self.alasan_text.delete("1.0", "end")

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.config(state="disabled")
        self.activity_list.delete(0, "end")
        self.nama_entry.focus_set()

    def show_about(self):
        about = tk.Toplevel(self.root)
        about.title("About")
        about.geometry("350x190")
        about.resizable(False, False)
        about.transient(self.root)

        ttk.Label(
            about,
            text="Aplikasi Pendaftaran Kegiatan Mahasiswa",
            font=("Arial", 11, "bold"),
            wraplength=310,
            justify="center"
        ).pack(pady=(22, 10))
        ttk.Label(
            about,
            text="Praktikum Python Tkinter – Sesi 11\n"
                 "Materi: Advanced Widgets dan Event Handling\n"
                 "Dibuat menggunakan Python dan Tkinter.",
            justify="center"
        ).pack(pady=5)
        ttk.Button(about, text="Tutup", command=about.destroy).pack(pady=12)

    def exit_app(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar dari aplikasi?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PendaftaranApp(root)
    root.mainloop()
