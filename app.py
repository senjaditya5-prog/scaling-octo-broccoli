import os
from datetime import date
import pandas as pd
import streamlit as st
from supabase import create_client

st.set_page_config(page_title="Kaloka", page_icon="💼", layout="wide")

st.markdown("""
<style>
/* Kaloka — modern dashboard theme */
:root {
  --bk-ink: #14213d;
  --bk-muted: #667085;
  --bk-teal: #0f9f91;
  --bk-teal-dark: #087f73;
  --bk-line: #e5eaf1;
  --bk-panel: #ffffff;
}
[data-testid="stAppViewContainer"] { background: #f4f7fb; }
[data-testid="stHeader"] { background: rgba(244,247,251,.88); }
[data-testid="stMain"] .block-container { max-width: 1440px; padding-top: 2rem; padding-bottom: 3rem; }
[data-testid="stAppViewContainer"]::before { content: ""; position: fixed; top: 0; left: 0; right: 0; height: 4px; z-index: 999999; background: linear-gradient(90deg,#0f9f91 0%,#42c7b8 55%,#91e3d9 100%); }
h1, h2, h3 { color: var(--bk-ink) !important; letter-spacing: -.025em; }
h1 { font-weight: 750 !important; }
p, label, [data-testid="stCaptionContainer"] { color: var(--bk-muted); }
/* Hide the old sidebar; navigation now lives at the top. */
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none !important; }
.bk-topbar { background:linear-gradient(120deg,#f4c542 0%,#f8d85f 60%,#ffe78a 100%); border:1px solid #e9b92f; border-radius:18px; padding:20px 26px; margin:0 0 14px; display:flex; align-items:center; gap:14px; box-shadow:0 10px 24px rgba(142,103,10,.13); }
.bk-topbar-mark { width:48px; height:48px; border-radius:14px; display:flex; align-items:center; justify-content:center; background:#172b3a; color:#f8d45b; font-size:25px; font-weight:800; flex-shrink:0; }
.bk-topbar-title { color:#172b3a; font-size:21px; font-weight:850; letter-spacing:.08em; line-height:1.2; }
.bk-topbar-sub { color:#55440d; font-size:11px; font-weight:650; letter-spacing:.16em; margin-top:5px; }
.bk-nav-wrap { background:#fff; border:1px solid #e5eaf1; border-radius:14px; padding:8px 12px 0; margin-bottom:24px; box-shadow:0 5px 16px rgba(18,36,64,.035); }
[data-testid="stRadio"] > label { display:none; }
[data-testid="stRadio"] [role="radiogroup"] { gap:8px; flex-wrap:wrap; }
[data-testid="stRadio"] [role="radio"] { border:1px solid transparent; border-radius:10px; padding:9px 13px; min-height:42px; }
[data-testid="stRadio"] [role="radio"] > div:first-child { display:none; }
[data-testid="stRadio"] [role="radio"] p { font-weight:650; color:#536273; white-space:nowrap; font-size:14px; }
[data-testid="stRadio"] [role="radio"] { background:#ffffff; transition:all .15s ease; }
[data-testid="stRadio"] [role="radio"]:hover { background:#fff9e6; border-color:#f0cf56; }
[data-testid="stRadio"] [role="radio"][aria-checked="true"] { background:#fff1b8; border-color:#e6bd28; box-shadow:0 2px 7px rgba(142,103,10,.10); }
[data-testid="stRadio"] [role="radio"][aria-checked="true"] p { color:#6d4e00 !important; }
.st-key-top_logout button { background:#ffffff !important; color:#172b3a !important; border:1px solid #e5eaf1 !important; }
.st-key-top_logout button:hover { background:#fff1b8 !important; border-color:#e6bd28 !important; color:#6d4e00 !important; }
.bk-page-heading { margin:0 0 20px; }
.bk-page-heading h1 { margin-bottom:4px; }
.bk-page-heading p { margin-top:0; }
[data-testid="stMetric"] { background: var(--bk-panel); border: 1px solid var(--bk-line); border-radius: 16px; padding: 18px 20px; box-shadow: 0 5px 18px rgba(18,36,64,.045); }
.bk-hero { background: linear-gradient(120deg,#111827 0%,#1e293b 68%,#123d43 100%); border-radius: 20px; padding: 24px 28px; color: #fff; margin: 0 0 24px 0; box-shadow: 0 12px 28px rgba(15,23,42,.12); }
.bk-brand-row { display:flex; align-items:center; gap:14px; }
.bk-brand-mark { width:48px; height:48px; border-radius:14px; display:flex; align-items:center; justify-content:center; background:#14b8a6; color:#062d2b; font-size:25px; font-weight:800; flex-shrink:0; }
.bk-brand-title { color:#fff; font-size:21px; font-weight:800; letter-spacing:.08em; line-height:1.2; }
.bk-brand-sub { color:#cbd5e1; font-size:11px; letter-spacing:.16em; margin-top:5px; }
.bk-hero-tag { color:#99f6e4; font-size:12px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; margin-top:20px; }
.bk-hero-heading { color:#fff; font-size:30px; font-weight:800; letter-spacing:-.04em; margin-top:5px; }
.bk-hero-desc { color:#cbd5e1; font-size:14px; margin-top:4px; }
.bk-stat { background:#fff; border:1px solid #e5eaf1; border-radius:17px; padding:20px; min-height:145px; box-shadow:0 6px 20px rgba(18,36,64,.045); }
.bk-stat-top { display:flex; align-items:center; justify-content:space-between; gap:8px; }
.bk-stat-label { color:#667085; font-size:13px; font-weight:650; }
.bk-stat-icon { width:38px; height:38px; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:19px; }
.bk-stat-value { color:#14213d; font-size:26px; font-weight:800; letter-spacing:-.03em; margin-top:16px; overflow-wrap:anywhere; }
.bk-stat-note { color:#98a2b3; font-size:11px; margin-top:5px; }
.bk-section-head { display:flex; justify-content:space-between; align-items:center; gap:10px; margin:26px 0 10px; }
.bk-section-title { color:#14213d; font-size:18px; font-weight:750; }

[data-testid="stMetricLabel"] { color: #667085 !important; font-size: .88rem; font-weight: 600; }
[data-testid="stMetricValue"] { color: var(--bk-ink) !important; font-weight: 750; }
[data-testid="stForm"] { background: #fff; border: 1px solid var(--bk-line); border-radius: 16px; padding: 1.2rem 1.25rem; box-shadow: 0 5px 18px rgba(18,36,64,.035); }
[data-testid="stTextInput"] input, [data-testid="stNumberInput"] input, [data-testid="stDateInput"] input, [data-testid="stSelectbox"] [data-baseweb="select"] > div, [data-testid="stTextArea"] textarea { border-radius: 10px !important; border-color: #d7deea !important; background: #fff !important; }
.stButton > button, [data-testid="stFormSubmitButton"] button, [data-testid="stDownloadButton"] button { border-radius: 10px; min-height: 2.65rem; font-weight: 650; border: 1px solid var(--bk-teal); background: var(--bk-teal); color: white; transition: all .15s ease; }
.stButton > button:hover, [data-testid="stFormSubmitButton"] button:hover, [data-testid="stDownloadButton"] button:hover { background: var(--bk-teal-dark); border-color: var(--bk-teal-dark); color: white; box-shadow: 0 5px 14px rgba(15,159,145,.2); }
[data-testid="stTabs"] [role="tablist"] { gap: .35rem; border-bottom: 1px solid var(--bk-line); }
[data-testid="stTabs"] button[role="tab"] { border-radius: 10px 10px 0 0; padding: .65rem 1rem; font-weight: 650; }
[data-testid="stTabs"] button[aria-selected="true"] { color: var(--bk-teal-dark) !important; border-bottom-color: var(--bk-teal) !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid var(--bk-line); border-radius: 12px; overflow: hidden; background: #fff; }
[data-testid="stAlert"] { border-radius: 12px; }
[data-testid="stExpander"] { background: #fff; border: 1px solid var(--bk-line); border-radius: 12px; }
hr { border-color: var(--bk-line); }
@media (max-width: 700px) {
  [data-testid="stMain"] .block-container { padding: 1.2rem .9rem 2rem; }
  [data-testid="stMetric"] { padding: 13px; }
}
</style>
""", unsafe_allow_html=True)

# Set these in Streamlit Cloud > App settings > Secrets, never in public source code.
def secret(key, default=None):
    # Local PowerShell environment variables first; Streamlit Secrets as cloud fallback.
    env_value = os.getenv(key)
    if env_value:
        return env_value
    try:
        return st.secrets[key]
    except Exception:
        return default


def rupiah(value):
    return "Rp " + f"{float(value or 0):,.0f}".replace(",", ".")


def require_login():
    password = secret("ADMIN_PASSWORD")
    if not password:
        st.error("ADMIN_PASSWORD belum dikonfigurasi di Streamlit Secrets.")
        st.stop()
    if st.session_state.get("logged_in"):
        return
    st.title("💼 Kaloka")
    st.caption("Silakan masuk sebagai administrator")
    with st.form("login"):
        entered = st.text_input("Password admin", type="password")
        submitted = st.form_submit_button("Masuk", use_container_width=True)
    if submitted:
        import hmac
        if hmac.compare_digest(entered, str(password)):
            st.session_state["logged_in"] = True
            st.rerun()
        st.error("Password salah.")
    st.stop()


require_login()
url = secret("SUPABASE_URL")
key = secret("SUPABASE_SERVICE_ROLE_KEY")
if not url or not key:
    st.error("Konfigurasi Supabase belum lengkap. Atur SUPABASE_URL dan SUPABASE_SERVICE_ROLE_KEY.")
    st.stop()
db = create_client(url, key)


def members_df():
    return pd.DataFrame(db.table("members").select("*").order("member_code").execute().data or [])


def transactions_df(start=None, end=None):
    query = db.table("transactions").select("*").order("transaction_date", desc=True)
    if start:
        query = query.gte("transaction_date", str(start))
    if end:
        query = query.lte("transaction_date", str(end))
    return pd.DataFrame(query.execute().data or [])


def rates_df():
    return pd.DataFrame(db.table("commission_rates").select("*").order("level").execute().data or [])


def member_label(row):
    return f"{row['member_code']} — {row['full_name']}"


def compute_payouts(amount, origin_id, members, rates):
    """Level 1 is the source member's direct sponsor, level 2 the sponsor above, etc."""
    if members.empty or rates.empty:
        return []
    by_id = {str(row["id"]): row for row in members.to_dict("records")}
    pct_by_level = {int(row["level"]): float(row["percentage"]) for row in rates.to_dict("records")}
    current = by_id.get(str(origin_id))
    seen = {str(origin_id)}
    level, payouts = 1, []
    while current and current.get("sponsor_id") and level <= 50:
        sponsor_id = str(current["sponsor_id"])
        if sponsor_id in seen:  # Defensive guard against a malformed sponsor loop.
            break
        seen.add(sponsor_id)
        sponsor = by_id.get(sponsor_id)
        if not sponsor:
            break
        pct = pct_by_level.get(level, 0.0)
        payouts.append({
            "recipient_id": sponsor["id"],
            "recipient_name": sponsor["full_name"],
            "recipient_code": sponsor["member_code"],
            "level": level,
            "percentage": pct,
            "commission_amount": round(float(amount) * pct / 100, 2),
        })
        current, level = sponsor, level + 1
    return payouts


# Brand header and horizontal top navigation, matching the requested preview.
st.markdown("""
<div class="bk-topbar">
  <div class="bk-topbar-mark">↗</div>
  <div>
    <div class="bk-topbar-title">KALOKA</div>
    <div class="bk-topbar-sub">BUSINESS MANAGEMENT SYSTEM</div>
  </div>
</div>
""", unsafe_allow_html=True)
nav_col, logout_col = st.columns([8, 1], vertical_alignment="center")
with nav_col:
    st.markdown('<div class="bk-nav-wrap">', unsafe_allow_html=True)
    selected_page = st.radio(
        "Navigasi utama",
        ["📊 Dashboard", "👥 Anggota", "🧾 Transaksi", "📈 Laporan", "⚙️ Pengaturan Komisi"],
        horizontal=True,
        label_visibility="collapsed",
        key="top_navigation",
    )
    # Keep internal page names unchanged so all existing features continue to work.
    page = selected_page.split(" ", 1)[1]
    st.markdown('</div>', unsafe_allow_html=True)
with logout_col:
    if st.button("↪ Keluar", use_container_width=True, key="top_logout"):
        st.session_state["logged_in"] = False
        st.rerun()

if page == "Dashboard":
    members = members_df()
    tx = transactions_df()
    total_value = pd.to_numeric(tx.get("amount", pd.Series(dtype=float)), errors="coerce").fillna(0).sum() if not tx.empty else 0
    payout_rows = db.table("commission_payouts").select("commission_amount").execute().data or []
    total_commission = sum(float(r.get("commission_amount") or 0) for r in payout_rows)
    transaction_count = len(tx)

    st.markdown("""
    <div class="bk-page-heading">
      <div style="color:#0f9f91;font-size:12px;font-weight:750;letter-spacing:.09em;text-transform:uppercase">Ringkasan bisnis</div>
      <h1 style="font-size:30px;font-weight:800;color:#14213d;margin:5px 0 4px">Dashboard</h1>
      <p style="font-size:14px;color:#667085;margin:0">Pantau anggota, transaksi, dan komisi dalam satu tempat.</p>
    </div>
    """, unsafe_allow_html=True)

    cards = [
        ("Total Komisi", rupiah(total_commission), "Jumlah komisi yang tercatat", "◈", "#ccfbf1", "#0f766e"),
        ("Total Anggota", f"{len(members):,}".replace(",", "."), "Anggota terdaftar", "♙", "#dbeafe", "#1d4ed8"),
        ("Total Transaksi", f"{transaction_count:,}".replace(",", "."), "Transaksi tersimpan", "▤", "#ede9fe", "#6d28d9"),
        ("Nilai Transaksi", rupiah(total_value), "Akumulasi nilai transaksi", "↗", "#ffedd5", "#c2410c"),
    ]
    cols = st.columns(4, gap="medium")
    for i, (label, value, note, symbol, bg, fg) in enumerate(cards):
        with cols[i]:
            st.markdown(f"""
            <div class="bk-stat">
              <div class="bk-stat-top"><div class="bk-stat-label">{label}</div><div class="bk-stat-icon" style="background:{bg};color:{fg}">{symbol}</div></div>
              <div class="bk-stat-value">{value}</div>
              <div class="bk-stat-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    left, right = st.columns([1.35, 1], gap="large")
    with left:
        st.markdown('<div class="bk-section-head"><div class="bk-section-title">Performa transaksi</div></div>', unsafe_allow_html=True)
        if not tx.empty and "transaction_date" in tx.columns and "amount" in tx.columns:
            chart_df = tx[["transaction_date", "amount"]].copy()
            chart_df["transaction_date"] = pd.to_datetime(chart_df["transaction_date"], errors="coerce")
            chart_df["amount"] = pd.to_numeric(chart_df["amount"], errors="coerce").fillna(0)
            chart_df = chart_df.dropna(subset=["transaction_date"])
            if not chart_df.empty:
                chart_df["Bulan"] = chart_df["transaction_date"].dt.to_period("M").astype(str)
                monthly = chart_df.groupby("Bulan", as_index=True)["amount"].sum().tail(8)
                st.bar_chart(monthly, use_container_width=True)
            else:
                st.info("Belum ada tanggal transaksi yang dapat ditampilkan pada grafik.")
        else:
            st.info("Grafik akan tampil setelah transaksi pertama disimpan.")
    with right:
        st.markdown('<div class="bk-section-head"><div class="bk-section-title">Komisi bertingkat</div></div>', unsafe_allow_html=True)
        try:
            rates = rates_df()
            if not rates.empty:
                rate_view = rates.copy()
                rate_view["Tarif"] = rate_view["percentage"].apply(lambda x: f"{float(x):g}%")
                rate_view["Level"] = rate_view["level"].apply(lambda x: f"Level {int(x)}")
                st.dataframe(rate_view[["Level", "Tarif"]], use_container_width=True, hide_index=True)
            else:
                st.info("Atur persentase komisi pada menu Pengaturan Komisi.")
        except Exception:
            st.info("Atur persentase komisi pada menu Pengaturan Komisi.")

    st.markdown('<div class="bk-section-head"><div class="bk-section-title">Transaksi terbaru</div></div>', unsafe_allow_html=True)
    if tx.empty:
        st.info("Belum ada transaksi. Tambahkan transaksi pertama melalui menu Transaksi.")
    else:
        st.dataframe(tx.head(8), use_container_width=True, hide_index=True)

elif page == "Anggota":
    st.title("Data Anggota")
    members = members_df()
    labels = {member_label(r): r["id"] for r in members.to_dict("records")} if not members.empty else {}
    tab_add, tab_edit = st.tabs(["Tambah anggota", "Cari / edit anggota"])
    with tab_add:
        with st.form("add_member"):
            code = st.text_input("Kode anggota", placeholder="A001")
            name = st.text_input("Nama lengkap")
            phone = st.text_input("Telepon (opsional)")
            sponsor_label = st.selectbox("Sponsor / perekrut", ["— Tidak ada —"] + list(labels))
            save = st.form_submit_button("Simpan anggota", use_container_width=True)
        if save:
            if not code.strip() or not name.strip():
                st.error("Kode anggota dan nama wajib diisi.")
            elif not members.empty and members["member_code"].astype(str).str.casefold().eq(code.strip().casefold()).any():
                st.error("Kode anggota sudah digunakan.")
            else:
                sponsor_id = None if sponsor_label == "— Tidak ada —" else labels[sponsor_label]
                try:
                    db.table("members").insert({"member_code": code.strip(), "full_name": name.strip(), "phone": phone.strip() or None, "sponsor_id": sponsor_id}).execute()
                    st.success("Anggota disimpan.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Gagal menyimpan: {exc}")
    with tab_edit:
        search = st.text_input("Cari kode atau nama")
        filtered = members.copy()
        if not filtered.empty and search:
            mask = filtered["member_code"].astype(str).str.contains(search, case=False, na=False) | filtered["full_name"].astype(str).str.contains(search, case=False, na=False)
            filtered = filtered[mask]
        if filtered.empty:
            st.info("Tidak ada anggota yang cocok.")
        else:
            st.dataframe(filtered[["member_code", "full_name", "phone", "sponsor_id"]], use_container_width=True, hide_index=True)
            selected_id = st.selectbox("Pilih anggota", filtered["id"].tolist(), format_func=lambda mid: member_label(members.loc[members["id"] == mid].iloc[0].to_dict()))
            row = members.loc[members["id"] == selected_id].iloc[0].to_dict()
            others = members[members["id"] != selected_id]
            other_labels = {member_label(r): r["id"] for r in others.to_dict("records")}
            sponsor_values = [None] + list(other_labels.values())
            current_sponsor = row.get("sponsor_id")
            sponsor_index = sponsor_values.index(current_sponsor) if current_sponsor in sponsor_values else 0
            with st.form("edit_member"):
                new_code = st.text_input("Kode anggota", value=str(row["member_code"]))
                new_name = st.text_input("Nama lengkap", value=str(row["full_name"]))
                new_phone = st.text_input("Telepon", value=str(row.get("phone") or ""))
                new_sponsor = st.selectbox("Sponsor", sponsor_values, index=sponsor_index, format_func=lambda x: "— Tidak ada —" if x is None else next((k for k, v in other_labels.items() if v == x), str(x)))
                update = st.form_submit_button("Simpan perubahan")
            if update:
                if not new_code.strip() or not new_name.strip():
                    st.error("Kode dan nama wajib diisi.")
                else:
                    # Prevent making a descendant the sponsor of its own ancestor.
                    descendant_ids, frontier = set(), [str(selected_id)]
                    while frontier:
                        parent = frontier.pop()
                        children = members[members["sponsor_id"].astype(str) == parent]
                        for child_id in children["id"].astype(str).tolist():
                            if child_id not in descendant_ids:
                                descendant_ids.add(child_id)
                                frontier.append(child_id)
                    if new_sponsor is not None and str(new_sponsor) in descendant_ids:
                        st.error("Sponsor tidak boleh dipilih dari jaringan bawah anggota ini karena akan membentuk siklus.")
                    else:
                        try:
                            db.table("members").update({"member_code": new_code.strip(), "full_name": new_name.strip(), "phone": new_phone.strip() or None, "sponsor_id": new_sponsor}).eq("id", selected_id).execute()
                            st.success("Data diperbarui.")
                            st.rerun()
                        except Exception as exc:
                            st.error(f"Gagal memperbarui: {exc}")

elif page == "Transaksi":
    st.title("Transaksi")
    members, rates = members_df(), rates_df()
    labels = {member_label(r): r["id"] for r in members.to_dict("records")} if not members.empty else {}
    if not labels:
        st.warning("Tambahkan anggota terlebih dahulu.")
    else:
        with st.form("transaction_form"):
            tx_date = st.date_input("Tanggal transaksi", value=date.today())
            tx_code = st.text_input("Nomor transaksi", placeholder="TRX-0001")
            origin_label = st.selectbox("Anggota sumber hasil", list(labels))
            amount = st.number_input("Nilai hasil dasar komisi (Rp)", min_value=1_000, step=100_000, value=1_000_000)
            description = st.text_input("Keterangan (opsional)")
            save_tx = st.form_submit_button("Simpan transaksi & hitung komisi", use_container_width=True)
        if save_tx:
            if not tx_code.strip():
                st.error("Nomor transaksi wajib diisi.")
            else:
                try:
                    existing = db.table("transactions").select("id").eq("transaction_code", tx_code.strip()).execute().data or []
                    if existing:
                        st.error("Nomor transaksi sudah digunakan.")
                    else:
                        origin_id = labels[origin_label]
                        created = db.table("transactions").insert({"transaction_code": tx_code.strip(), "transaction_date": str(tx_date), "origin_member_id": origin_id, "amount": float(amount), "description": description.strip() or None}).execute().data
                        transaction_id = created[0]["id"]
                        payouts = compute_payouts(amount, origin_id, members, rates)
                        if payouts:
                            db.table("commission_payouts").insert([{**p, "transaction_id": transaction_id} for p in payouts]).execute()
                        st.success(f"Transaksi tersimpan. {len(payouts)} penerima komisi dihitung.")
                        if payouts:
                            view = pd.DataFrame(payouts)
                            view["commission_amount"] = view["commission_amount"].apply(rupiah)
                            st.dataframe(view, use_container_width=True, hide_index=True)
                        else:
                            st.info("Tidak ada upline di atas anggota sumber, atau belum ada tarif komisi.")
                except Exception as exc:
                    st.error(f"Transaksi gagal disimpan: {exc}. Periksa tabel Supabase dan koneksi.")
    st.subheader("Riwayat transaksi")
    tx = transactions_df()
    if tx.empty:
        st.info("Belum ada transaksi.")
    else:
        st.dataframe(tx, use_container_width=True, hide_index=True)

elif page == "Laporan":
    st.title("Laporan")
    left, right = st.columns(2)
    start = left.date_input("Dari tanggal", value=date.today().replace(day=1))
    end = right.date_input("Sampai tanggal", value=date.today())
    if start > end:
        st.error("Tanggal awal harus sebelum atau sama dengan tanggal akhir.")
        st.stop()
    tx = transactions_df(start, end)
    if tx.empty:
        st.info("Tidak ada transaksi dalam periode ini.")
    else:
        st.subheader("Transaksi")
        st.dataframe(tx, use_container_width=True, hide_index=True)
        st.download_button("Unduh transaksi CSV", tx.to_csv(index=False).encode("utf-8-sig"), file_name=f"transaksi_{start}_{end}.csv", mime="text/csv")
        tx_ids = tx["id"].astype(str).tolist()
        payout_rows = db.table("commission_payouts").select("*").execute().data or []
        payouts = pd.DataFrame(payout_rows)
        if not payouts.empty:
            payouts["transaction_id"] = payouts["transaction_id"].astype(str)
            payouts = payouts[payouts["transaction_id"].isin(tx_ids)]
        st.subheader("Komisi")
        if payouts.empty:
            st.info("Belum ada komisi tercatat untuk transaksi dalam periode ini.")
        else:
            st.metric("Total komisi periode", rupiah(pd.to_numeric(payouts["commission_amount"], errors="coerce").fillna(0).sum()))
            payouts = payouts.merge(tx[["id", "transaction_code", "transaction_date", "amount"]], left_on="transaction_id", right_on="id", how="left")
            st.dataframe(payouts, use_container_width=True, hide_index=True)
            st.download_button("Unduh komisi CSV", payouts.to_csv(index=False).encode("utf-8-sig"), file_name=f"komisi_{start}_{end}.csv", mime="text/csv")

elif page == "Pengaturan Komisi":
    st.title("Pengaturan Komisi Bertingkat")
    st.caption("Level 1 = sponsor langsung anggota sumber hasil; level 2 = sponsor di atasnya, dan seterusnya.")
    rates = rates_df()
    if not rates.empty:
        st.dataframe(rates, use_container_width=True, hide_index=True)
    with st.form("rate_form"):
        level = st.number_input("Level upline", min_value=1, max_value=50, value=1, step=1)
        percentage = st.number_input("Persentase (%)", min_value=0.0, max_value=100.0, value=6.0, step=0.5)
        save_rate = st.form_submit_button("Simpan persentase")
    if save_rate:
        try:
            db.table("commission_rates").upsert({"level": int(level), "percentage": float(percentage)}, on_conflict="level").execute()
            st.success("Persentase tersimpan. Tarif baru berlaku untuk transaksi berikutnya.")
            st.rerun()
        except Exception as exc:
            st.error(f"Gagal menyimpan persentase: {exc}")
