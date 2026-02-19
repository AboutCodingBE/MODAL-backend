import streamlit as st

from components.archive_storage import ArchiveStorage
from components.archive_creation_controller import ArchiveCreationController
from components.archive_list_controller import ArchiveListController
from components.archive_detail_controller import ArchiveDetailController

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MODAL",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "archives" not in st.session_state:
    st.session_state.archives = {}
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}
if "current_view" not in st.session_state:
    st.session_state.current_view = "list"
if "selected_archive_id" not in st.session_state:
    st.session_state.selected_archive_id = None
if "current_folder" not in st.session_state:
    st.session_state.current_folder = "/"

# ── Controllers ───────────────────────────────────────────────────────────────
storage = ArchiveStorage(st.session_state.archives, st.session_state.analysis_results)
creation_ctrl = ArchiveCreationController(storage)
list_ctrl = ArchiveListController(storage)
detail_ctrl = ArchiveDetailController(storage)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Reset & hide chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0f172a !important;
    min-width: 220px !important;
    max-width: 220px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
}
/* kill the default top padding inside sidebar content */
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown span,
section[data-testid="stSidebar"] .stMarkdown div {
    color: #94a3b8 !important;
}
/* remove default collapse button border */
section[data-testid="stSidebar"] button[kind="header"] {
    display: none;
}

/* ── Main block container ── */
.block-container {
    padding-top: 2rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 100% !important;
    background-color: #f8fafc;
}

/* ── Archive cards ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    padding: 4px !important;
    transition: box-shadow 0.2s !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.10) !important;
}

/* ── "Resultaten" button inside card – light style ── */
div[data-testid="stVerticalBlockBorderWrapper"] .stButton button {
    background-color: #f1f5f9 !important;
    color: #334155 !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 7px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    width: 100% !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] .stButton button:hover {
    background-color: #e2e8f0 !important;
}

/* ── "Analyse Starten" – dark style (secondary class workaround) ── */
.analyse-btn button {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 7px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    width: 100% !important;
}
.analyse-btn button:hover {
    background-color: #334155 !important;
}

/* ── Top-right "Nieuw Archief" button ── */
.top-action .stButton button {
    background-color: #3b82f6 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    font-size: 14px !important;
}
.top-action .stButton button:hover {
    background-color: #2563eb !important;
}

/* ── Detail back button ── */
.back-btn button {
    background-color: transparent !important;
    color: #3b82f6 !important;
    border: 1px solid #bfdbfe !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}

/* ── Breadcrumb buttons ── */
.breadcrumb-btn button {
    background-color: transparent !important;
    color: #3b82f6 !important;
    border: none !important;
    padding: 2px 6px !important;
    font-size: 13px !important;
    min-height: 0 !important;
}

/* ── Subfolder buttons ── */
.subfolder-btn button {
    background-color: #f8fafc !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 7px !important;
    font-size: 13px !important;
    text-align: left !important;
    width: 100% !important;
}
.subfolder-btn button:hover {
    background-color: #eff6ff !important;
    border-color: #bfdbfe !important;
    color: #1d4ed8 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 16px 16px; border-bottom:1px solid #1e293b; margin-bottom:8px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="background:#3b82f6;color:#fff;font-weight:700;
                        width:32px;height:32px;border-radius:6px;
                        display:flex;align-items:center;justify-content:center;font-size:16px;">
                M
            </div>
            <span style="color:#f1f5f9;font-size:16px;font-weight:600;letter-spacing:.01em;">
                MODAL
            </span>
        </div>
    </div>

    <div style="padding:8px 12px;">
        <div style="background:#3b82f6;border-radius:8px;padding:9px 12px;
                    display:flex;align-items:center;gap:10px;margin-bottom:2px;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                 stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
                <rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>
            </svg>
            <span style="color:#fff;font-size:14px;font-weight:500;">Archieven</span>
        </div>

        <div style="padding:9px 12px;display:flex;align-items:center;gap:10px;
                    border-radius:8px;margin-bottom:2px;cursor:default;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                 stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <span style="color:#64748b;font-size:14px;">Zoeken</span>
        </div>

        <div style="padding:9px 12px;display:flex;align-items:center;gap:10px;
                    border-radius:8px;cursor:default;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                 stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="3"/>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"/>
            </svg>
            <span style="color:#64748b;font-size:14px;">Configuratie</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Modal: create archive ─────────────────────────────────────────────────────
@st.dialog("Nieuw Archief Toevoegen")
def create_archive_dialog():
    st.markdown("""
    <style>
    div[data-testid="stDialog"] [data-testid="stVerticalBlock"] label {
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: .06em !important;
        color: #64748b !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stDialog"] .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
        font-size: 14px !important;
    }
    div[data-testid="stDialog"] .stButton button {
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    archive_name = st.text_input(
        "Naam van het archief",
        placeholder="Bijv. Project_Antwerpen_2026",
        key="dlg_archive_name",
    )

    col_path, col_sel = st.columns([3, 1])
    with col_path:
        folder_path = st.text_input(
            "Locatie op schijf",
            placeholder="/pad/naar/map",
            key="dlg_folder_path",
        )
    with col_sel:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        st.button("Select Folder", key="dlg_select_folder", disabled=True, help="Typ het pad handmatig in")

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    col_cancel, col_submit = st.columns(2)
    with col_cancel:
        if st.button("Annuleren", use_container_width=True, key="dlg_cancel"):
            st.rerun()
    with col_submit:
        if st.button("Archief Ingesten", type="primary", use_container_width=True, key="dlg_submit"):
            with st.spinner("Archief aanmaken…"):
                archive_id, error = creation_ctrl.create(archive_name, folder_path)
            if error:
                st.error(error)
            else:
                st.success(f"Archief '{archive_name}' aangemaakt!")
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# VIEW: LIST
# ═══════════════════════════════════════════════════════════════════════════════
def render_list_view():
    # Header row
    col_title, _, col_btn = st.columns([5, 2, 1])
    with col_title:
        st.markdown("""
        <h1 style="font-size:22px;font-weight:700;color:#1e293b;margin:0 0 2px 0;">
            Archive Browser
        </h1>
        <p style="color:#94a3b8;font-size:13px;margin:0 0 24px 0;">
            Beheer en verken uw digitale collecties
        </p>
        """, unsafe_allow_html=True)
    with col_btn:
        st.markdown('<div class="top-action">', unsafe_allow_html=True)
        if st.button("＋  Nieuw Archief", key="open_dialog"):
            create_archive_dialog()
        st.markdown('</div>', unsafe_allow_html=True)

    archives = list_ctrl.get_archives()

    if not archives:
        st.markdown("""
        <div style="text-align:center;padding:80px 0;color:#94a3b8;">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
                 stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"
                 stroke-linejoin="round" style="margin-bottom:12px;">
                <ellipse cx="12" cy="5" rx="9" ry="3"/>
                <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
            </svg>
            <p style="font-size:15px;margin:0;">Geen archieven gevonden.</p>
            <p style="font-size:13px;margin:4px 0 0;">
                Klik op <strong>＋ Nieuw Archief</strong> om te beginnen.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Cards grid – 3 columns
    cols = st.columns(3, gap="medium")
    for i, archive in enumerate(archives):
        with cols[i % 3]:
            _render_archive_card(archive)


def _badge(status: str) -> str:
    if status == "ready":
        return ('<span style="background:#dcfce7;color:#16a34a;font-size:10px;font-weight:700;'
                'letter-spacing:.06em;padding:3px 9px;border-radius:20px;text-transform:uppercase;">'
                'ANALYSED</span>')
    return ('<span style="background:#dbeafe;color:#2563eb;font-size:10px;font-weight:700;'
            'letter-spacing:.06em;padding:3px 9px;border-radius:20px;text-transform:uppercase;">'
            'INGESTED</span>')


def _render_archive_card(archive: dict):
    status = archive["status"]
    date_str = archive["created_at"][:10]
    files_str = f"{archive['total_files']} bestanden" if archive["total_files"] is not None else "—"

    with st.container(border=True):
        # Card header: icon + badge
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:flex-start;
                    margin-bottom:10px;">
            <div style="background:#eff6ff;border-radius:9px;width:40px;height:40px;
                        display:flex;align-items:center;justify-content:center;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none"
                     stroke="#3b82f6" stroke-width="2" stroke-linecap="round"
                     stroke-linejoin="round">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
                    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
                </svg>
            </div>
            {_badge(status)}
        </div>

        <div style="font-size:15px;font-weight:600;color:#1e293b;margin-bottom:8px;
                    word-break:break-word;">
            {archive['name']}
        </div>

        <div style="font-size:12px;color:#64748b;display:flex;align-items:center;
                    gap:5px;margin-bottom:4px;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
                 stroke="#94a3b8" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
            </svg>
            {date_str}
        </div>
        <div style="font-size:12px;color:#64748b;display:flex;align-items:center;
                    gap:5px;margin-bottom:12px;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none"
                 stroke="#94a3b8" stroke-width="2" stroke-linecap="round"
                 stroke-linejoin="round">
                <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>
                <polyline points="13 2 13 9 20 9"/>
            </svg>
            {files_str}
        </div>
        """, unsafe_allow_html=True)

        if status == "ready":
            if st.button("Resultaten", key=f"res_{archive['archive_id']}", use_container_width=True):
                st.session_state.current_view = "detail"
                st.session_state.selected_archive_id = archive["archive_id"]
                st.session_state.current_folder = "/"
                st.rerun()
        else:
            st.markdown('<div class="analyse-btn">', unsafe_allow_html=True)
            if st.button("▶  Analyse Starten", key=f"ana_{archive['archive_id']}", use_container_width=True):
                with st.spinner(f"Analyseren van '{archive['name']}'…"):
                    err = creation_ctrl.run_analysis(archive["archive_id"])
                if err:
                    st.error(err)
                else:
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# VIEW: DETAIL
# ═══════════════════════════════════════════════════════════════════════════════
def render_detail_view():
    archive_id = st.session_state.selected_archive_id
    current_folder = st.session_state.get("current_folder", "/")
    detail = detail_ctrl.get_detail(archive_id, current_folder)

    if not detail:
        st.error("Archief niet gevonden.")
        if st.button("← Terug"):
            st.session_state.current_view = "list"
            st.rerun()
        return

    # ── Header ──
    col_back, col_title = st.columns([2, 8])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Lijst"):
            st.session_state.current_view = "list"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_title:
        st.markdown(f"""
        <h1 style="font-size:22px;font-weight:700;color:#1e293b;margin:0 0 2px 0;">
            {detail['name']}
        </h1>
        <p style="color:#94a3b8;font-size:13px;margin:0 0 20px 0;">{detail['path']}</p>
        """, unsafe_allow_html=True)

    # ── Summary metrics ──
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Totaal bestanden", detail["total_files"] or 0)
    with col2:
        st.metric("Aangemaakt", detail["created_at"][:10])
    with col3:
        unique_types = len(detail["file_types"]) if detail["file_types"] else 0
        st.metric("Bestandstypen", unique_types)

    # ── File type breakdown ──
    if detail["file_types"]:
        st.markdown("#### Bestandstypen")
        top = sorted(detail["file_types"].items(), key=lambda x: x[1], reverse=True)[:10]
        type_cols = st.columns(min(len(top), 5))
        for idx, (ext, count) in enumerate(top):
            with type_cols[idx % 5]:
                st.markdown(f"""
                <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
                            padding:10px 14px;text-align:center;margin-bottom:8px;">
                    <div style="font-size:12px;font-weight:700;color:#475569;">{ext}</div>
                    <div style="font-size:20px;font-weight:700;color:#1e293b;">{count}</div>
                </div>
                """, unsafe_allow_html=True)

    st.divider()

    # ── Folder browser ──
    st.markdown("#### Mapbrowser")

    # Breadcrumb
    parts = [p for p in current_folder.split("/") if p]
    crumb_cols = st.columns(max(len(parts) + 1, 1))
    with crumb_cols[0]:
        st.markdown('<div class="breadcrumb-btn">', unsafe_allow_html=True)
        if st.button("🏠 /", key="bc_root"):
            st.session_state.current_folder = "/"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    for idx, part in enumerate(parts):
        with crumb_cols[idx + 1]:
            path_to = "/" + "/".join(parts[:idx + 1])
            st.markdown('<div class="breadcrumb-btn">', unsafe_allow_html=True)
            if st.button(f"/ {part}", key=f"bc_{idx}"):
                st.session_state.current_folder = path_to
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    folder_info = detail.get("folder_info")
    if not folder_info:
        st.info("Geen mapinformatie beschikbaar voor dit pad.")
        return

    st.markdown(f"""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;
                padding:12px 16px;margin:8px 0 16px;">
        <span style="font-size:13px;color:#64748b;">
            📄 <strong>{folder_info['files_count']}</strong> bestanden direct in deze map
        </span>
    </div>
    """, unsafe_allow_html=True)

    subfolders = folder_info.get("subfolders", [])
    if subfolders:
        st.markdown(f"**{len(subfolders)} submappen**")
        sf_cols = st.columns(min(len(subfolders), 3))
        for idx, subfolder in enumerate(subfolders):
            parent = current_folder.rstrip("/")
            sub_path = f"{parent}/{subfolder}"
            with sf_cols[idx % 3]:
                st.markdown('<div class="subfolder-btn">', unsafe_allow_html=True)
                if st.button(f"📁  {subfolder}", key=f"sf_{idx}_{subfolder}", use_container_width=True):
                    st.session_state.current_folder = sub_path
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<p style="color:#94a3b8;font-size:13px;">Geen submappen in deze map.</p>',
            unsafe_allow_html=True,
        )


# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state.current_view == "detail":
    render_detail_view()
else:
    render_list_view()
