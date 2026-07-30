"""
video2image — Professional Desktop GUI
Photogrammetry & Frame Extraction Tool
"""

import glob
import os
import subprocess
import sys

import cv2
from PyQt6.QtCore import Qt, QSettings, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QActionGroup, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

try:
    from .converter import extract_frames, extract_frames_batch, find_videos_recursive
except ImportError:
    from converter import extract_frames, extract_frames_batch, find_videos_recursive

ORG_NAME = "video2image"
APP_NAME = "video2image"


def _resource_path(filename):
    """Resolve a bundled resource, whether running from source or a frozen PyInstaller build."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, filename)


def _get_version():
    """Resolve the app version without hardcoding it anywhere.

    Release builds ship a VERSION file that CI writes from the git tag that
    triggered the build (see .github/workflows/gui-release.yml), so the
    version shown always matches the actual release. Running from source has
    no such file, so it falls back to `git describe`, which never runs in a
    packaged .exe since the VERSION file short-circuits it first.
    """
    version_file = _resource_path("VERSION")
    if os.path.isfile(version_file):
        try:
            with open(version_file, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    return text
        except OSError:
            pass

    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--always", "--dirty"],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=True,
            text=True,
            timeout=3,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass

    return "dev"


VERSION = _get_version()

# ---------------------------------------------------------------------------
# Theme palettes — dark & light, tuned for WCAG-friendly contrast in both
# button-on-accent text (accent_text) and page text/backgrounds.
# ---------------------------------------------------------------------------
PALETTES = {
    "dark": {
        "bg": "#12131a",
        "surface": "#1a1c23",
        "surface2": "#232631",
        "border": "#2b2e3a",
        "text": "#e7e9f0",
        "text_muted": "#8b93ab",
        "accent": "#7aa2f7",
        "accent_text": "#0f1015",
        "success": "#9ece6a",
        "success_text": "#0f1015",
        "danger": "#f7768e",
        "danger_text": "#0f1015",
        "hover": "#262a36",
        "status_text": "#6b7394",
    },
    "light": {
        "bg": "#f2f3f7",
        "surface": "#ffffff",
        "surface2": "#eef0f6",
        "border": "#d8dce6",
        "text": "#1c1f2a",
        "text_muted": "#5b6377",
        "accent": "#3457d5",
        "accent_text": "#ffffff",
        "success": "#1f8a4c",
        "success_text": "#ffffff",
        "danger": "#c62a44",
        "danger_text": "#ffffff",
        "hover": "#e6e9f2",
        "status_text": "#6b7280",
    },
}


def build_stylesheet(p):
    """Render the full QSS stylesheet from a palette dict of color tokens."""
    return f"""
QMainWindow {{
    background-color: {p['bg']};
}}
QWidget {{
    color: {p['text']};
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-size: 12px;
}}

/* Header & Cards */
QFrame#header-card, QFrame#card {{
    background-color: {p['surface']};
    border: 1px solid {p['border']};
    border-radius: 6px;
}}

QLabel#section-title {{
    color: {p['accent']};
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

QLabel#info-icon {{
    color: {p['accent']};
    background-color: {p['surface2']};
    border: 1px solid {p['border']};
    border-radius: 7px;
    font-size: 10px;
    font-weight: 700;
    font-style: italic;
    font-family: Georgia, 'Times New Roman', serif;
    padding: 0px 5px;
    min-width: 10px;
    max-height: 14px;
    qproperty-alignment: AlignCenter;
}}
QLabel#info-icon:hover {{
    color: {p['accent_text']};
    background-color: {p['accent']};
    border-color: {p['accent']};
}}

QLabel#preset-desc {{
    color: {p['text_muted']};
    font-size: 11px;
    font-style: italic;
}}

/* Inputs & Form Controls */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: {p['bg']};
    border: 1px solid {p['border']};
    border-radius: 4px;
    padding: 5px 8px;
    color: {p['text']};
    selection-background-color: {p['accent']};
}}
QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover, QComboBox:hover {{
    border-color: {p['accent']};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 1px solid {p['accent']};
}}
QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {{
    color: {p['text_muted']};
    background-color: {p['surface2']};
    border-color: {p['border']};
}}
QLineEdit::placeholder {{
    color: {p['text_muted']};
}}

/* Combo box dropdown chevron */
QComboBox {{
    padding-right: 22px;
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 22px;
    border-left: 1px solid {p['border']};
}}
QComboBox::down-arrow {{
    image: none;
    width: 0px;
    height: 0px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {p['text_muted']};
    margin-right: 8px;
}}
QComboBox::down-arrow:on {{
    border-top-color: {p['accent']};
}}
QComboBox QAbstractItemView {{
    background-color: {p['surface']};
    color: {p['text']};
    selection-background-color: {p['hover']};
    selection-color: {p['text']};
    border: 1px solid {p['border']};
    border-radius: 4px;
    outline: none;
    padding: 2px;
}}
QComboBox QAbstractItemView::item {{
    padding: 5px 8px;
    border-radius: 3px;
    min-height: 18px;
}}

/* Spin box stepper buttons */
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 16px;
    border-left: 1px solid {p['border']};
    border-bottom: 1px solid {p['border']};
    border-top-right-radius: 4px;
    background-color: {p['surface2']};
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 16px;
    border-left: 1px solid {p['border']};
    border-bottom-right-radius: 4px;
    background-color: {p['surface2']};
}}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{
    background-color: {p['hover']};
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    image: none;
    width: 0px;
    height: 0px;
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-bottom: 4px solid {p['text_muted']};
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    image: none;
    width: 0px;
    height: 0px;
    border-left: 3px solid transparent;
    border-right: 3px solid transparent;
    border-top: 4px solid {p['text_muted']};
}}

/* Buttons */
QPushButton {{
    background-color: {p['surface2']};
    border: 1px solid {p['border']};
    border-radius: 4px;
    padding: 6px 12px;
    color: {p['text']};
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: {p['hover']};
    border-color: {p['accent']};
}}
QPushButton:pressed {{
    background-color: {p['bg']};
}}
QPushButton:disabled {{
    background-color: {p['bg']};
    color: {p['text_muted']};
    border-color: {p['border']};
}}

QPushButton#btn-primary {{
    background-color: {p['accent']};
    color: {p['accent_text']};
    font-weight: 700;
    padding: 6px 14px;
    border: none;
}}
QPushButton#btn-primary:hover {{
    background-color: {p['accent']};
}}

QPushButton#btn-start {{
    background-color: {p['success']};
    color: {p['success_text']};
    font-weight: 700;
    font-size: 13px;
    padding: 8px 24px;
    border: none;
    border-radius: 5px;
}}
QPushButton#btn-start:hover {{
    background-color: {p['success']};
}}
QPushButton#btn-start:disabled {{
    background-color: {p['surface2']};
    color: {p['text_muted']};
}}

QPushButton#btn-cancel {{
    background-color: {p['danger']};
    color: {p['danger_text']};
    font-weight: 700;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
}}
QPushButton#btn-cancel:hover {{
    background-color: {p['danger']};
}}
QPushButton#btn-cancel:disabled {{
    background-color: {p['surface2']};
    color: {p['text_muted']};
}}

QPushButton#theme-toggle {{
    background-color: transparent;
    border: 1px solid {p['border']};
    border-radius: 4px;
    font-size: 13px;
    padding: 1px;
}}
QPushButton#theme-toggle:hover {{
    background-color: {p['hover']};
    border-color: {p['accent']};
}}

/* Checkboxes */
QCheckBox {{
    spacing: 8px;
    color: {p['text']};
}}
QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border-radius: 3px;
    border: 1px solid {p['border']};
    background-color: {p['bg']};
}}
QCheckBox::indicator:hover {{
    border-color: {p['accent']};
}}
QCheckBox::indicator:checked {{
    background-color: {p['accent']};
    border-color: {p['accent']};
}}

/* Sliders */
QSlider::groove:horizontal {{
    height: 4px;
    background: {p['surface2']};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {p['accent']};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::sub-page:horizontal {{
    background: {p['accent']};
    border-radius: 2px;
}}

/* Progress bar */
QProgressBar {{
    background-color: {p['bg']};
    border: 1px solid {p['border']};
    border-radius: 4px;
    height: 18px;
    text-align: center;
    color: {p['text']};
    font-size: 11px;
    font-weight: 600;
}}
QProgressBar::chunk {{
    background-color: {p['accent']};
    border-radius: 3px;
}}

/* Menu Bar */
QMenuBar {{
    background-color: {p['bg']};
    color: {p['text']};
    border-bottom: 1px solid {p['border']};
    padding: 1px 4px;
}}
QMenuBar::item {{
    padding: 4px 8px;
    border-radius: 3px;
}}
QMenuBar::item:selected {{
    background-color: {p['surface']};
}}
QMenu {{
    background-color: {p['surface']};
    color: {p['text']};
    border: 1px solid {p['border']};
    border-radius: 4px;
    padding: 4px;
}}
QMenu::item {{
    padding: 5px 18px;
    border-radius: 3px;
}}
QMenu::item:selected {{
    background-color: {p['hover']};
}}
QMenu::separator {{
    height: 1px;
    background: {p['border']};
    margin: 3px 4px;
}}

/* Tooltips */
QToolTip {{
    background-color: {p['surface2']};
    color: {p['text']};
    border: 1px solid {p['accent']};
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 11px;
}}

/* Status Bar */
QStatusBar {{
    background-color: {p['bg']};
    color: {p['status_text']};
    border-top: 1px solid {p['border']};
    font-size: 11px;
}}
"""


# ---------------------------------------------------------------------------
# Photogrammetry quick presets — map a plain-language scenario to the
# scene/motion/keyframe settings a new user would otherwise have to guess.
# ---------------------------------------------------------------------------
CUSTOM_PRESET_NAME = "Custom (Manual Settings)"
PHOTOGRAMMETRY_PRESETS = {
    CUSTOM_PRESET_NAME: {
        "desc": "Manually configure every option below for full control.",
    },
    "🚁 Aerial / Drone Survey": {
        "keyframe": True,
        "frame_step": 2,
        "scene_threshold": 15.0,
        "motion_threshold": 3.0,
        "format": "png",
        "desc": "For steady, wide drone footage. Keeps closely-spaced, overlapping frames for dense point clouds.",
    },
    "🚶 Handheld Walkthrough": {
        "keyframe": True,
        "frame_step": 5,
        "scene_threshold": 20.0,
        "motion_threshold": 5.0,
        "format": "png",
        "desc": "For walking shots with natural hand shake. Filters out blurry and near-duplicate frames.",
    },
    "🔄 Turntable / Object Scan": {
        "keyframe": True,
        "frame_step": 3,
        "scene_threshold": 12.0,
        "motion_threshold": 2.0,
        "format": "png",
        "desc": "For objects rotating on a turntable. Captures small angular changes for full 360° coverage.",
    },
    "🏛 High-Detail Dense Scan": {
        "keyframe": False,
        "frame_step": 1,
        "scene_threshold": 30.0,
        "motion_threshold": 5.0,
        "format": "png",
        "desc": "Extracts every single frame at full quality. Produces large datasets — best for small scenes.",
    },
}


class ExtractionWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int)

    def __init__(self, video_paths, output_folder, kwargs, is_batch=False):
        super().__init__()
        self.video_paths = video_paths
        self.output_folder = output_folder
        self.kwargs = kwargs
        self.is_batch = is_batch

    def run(self):
        try:
            if self.is_batch:
                results = extract_frames_batch(
                    self.video_paths,
                    self.output_folder,
                    progress_callback=lambda cur, total: self.progress.emit(cur, total),
                    **self.kwargs,
                )
                ok = sum(1 for r in results if r.get("success"))
                self.finished.emit(f"Batch extraction complete: {ok}/{len(results)} videos processed.")
            else:
                result = extract_frames(
                    self.video_paths[0],
                    self.output_folder,
                    progress_callback=lambda cur, total: self.progress.emit(cur, total),
                    **self.kwargs,
                )
                self.finished.emit(f"Extraction complete!\nSaved to: {result}")
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video2Image")
        icon_path = _resource_path("logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.resize(880, 700)
        self.setMinimumSize(780, 600)
        self.worker = None
        self._max_workers = 4
        self.theme = self._load_theme_pref()

        self._build_menubar()
        self._build_ui()
        self._apply_theme(self.theme)
        self.statusBar().showMessage("Ready")

    # -----------------------------------------------------------------
    # Theme persistence
    # -----------------------------------------------------------------
    def _load_theme_pref(self):
        theme = QSettings(ORG_NAME, APP_NAME).value("theme", "dark")
        return theme if theme in PALETTES else "dark"

    def _apply_theme(self, name):
        self.theme = name
        p = PALETTES[name]
        self.setStyleSheet(build_stylesheet(p))
        self.info_label.setStyleSheet(f"color: {p['accent']}; font-weight: 600; font-size: 11px;")
        self.keyframe_check.setStyleSheet(f"color: {p['success']}; font-weight: 600;")

        is_dark = name == "dark"
        self.theme_btn.setText("☀" if is_dark else "🌙")
        self.theme_btn.setToolTip("Switch to light mode" if is_dark else "Switch to dark mode")
        self._act_theme_dark.setChecked(is_dark)
        self._act_theme_light.setChecked(not is_dark)

        QSettings(ORG_NAME, APP_NAME).setValue("theme", name)

    def _toggle_theme(self):
        self._apply_theme("light" if self.theme == "dark" else "dark")

    # -----------------------------------------------------------------
    # Info-icon / tooltip helpers
    # -----------------------------------------------------------------
    def _info_icon(self, tooltip):
        icon = QLabel("i")
        icon.setObjectName("info-icon")
        icon.setToolTip(tooltip)
        icon.setCursor(Qt.CursorShape.WhatsThisCursor)
        return icon

    def _field_label(self, text, tooltip):
        """A QFormLayout row label with a hoverable info icon beside it."""
        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(5)
        row.addWidget(QLabel(text))
        row.addWidget(self._info_icon(tooltip))
        row.addStretch()
        return container

    def _checkbox_row(self, checkbox, tooltip):
        """Wraps a checkbox with a matching tooltip and a visible info icon."""
        checkbox.setToolTip(tooltip)
        checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(5)
        row.addWidget(checkbox)
        row.addWidget(self._info_icon(tooltip))
        row.addStretch()
        return container

    def _build_menubar(self):
        mb = self.menuBar()

        file_m = mb.addMenu("&File")
        a1 = QAction("Open Video File…", self)
        a1.setShortcut("Ctrl+O")
        a1.triggered.connect(self._pick_file)
        file_m.addAction(a1)

        a2 = QAction("Open Video Directory…", self)
        a2.setShortcut("Ctrl+Shift+O")
        a2.triggered.connect(self._pick_input_dir)
        file_m.addAction(a2)

        file_m.addSeparator()
        a_exit = QAction("Exit", self)
        a_exit.setShortcut("Ctrl+Q")
        a_exit.triggered.connect(self.close)
        file_m.addAction(a_exit)

        batch_m = mb.addMenu("&Batch Settings")
        self._act_recursive = QAction("Recursive Directory Scan", self)
        self._act_recursive.setCheckable(True)
        batch_m.addAction(self._act_recursive)

        self._act_parallel = QAction("Parallel Video Processing", self)
        self._act_parallel.setCheckable(True)
        batch_m.addAction(self._act_parallel)

        batch_m.addSeparator()
        workers_sub = batch_m.addMenu("Max Parallel Workers")
        self._workers_actions = []
        for n in [1, 2, 4, 8, 16]:
            act = QAction(f"{n} Workers", self)
            act.setCheckable(True)
            act.setChecked(n == 4)
            act.triggered.connect(lambda checked, num=n: self._set_workers(num))
            workers_sub.addAction(act)
            self._workers_actions.append((n, act))

        view_m = mb.addMenu("&View")
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)

        self._act_theme_dark = QAction("Dark Theme", self)
        self._act_theme_dark.setCheckable(True)
        self._act_theme_dark.triggered.connect(lambda: self._apply_theme("dark"))
        theme_group.addAction(self._act_theme_dark)
        view_m.addAction(self._act_theme_dark)

        self._act_theme_light = QAction("Light Theme", self)
        self._act_theme_light.setCheckable(True)
        self._act_theme_light.triggered.connect(lambda: self._apply_theme("light"))
        theme_group.addAction(self._act_theme_light)
        view_m.addAction(self._act_theme_light)

        help_m = mb.addMenu("&Help")
        a_tips = QAction("Photogrammetry Workflow Tips", self)
        a_tips.triggered.connect(self._show_tips)
        help_m.addAction(a_tips)

        help_m.addSeparator()
        a_about = QAction("About Video2Image", self)
        a_about.triggered.connect(self._show_about)
        help_m.addAction(a_about)

        # Quick light/dark toggle, always visible in the top-right corner
        # of the main window — no need to dig through the View menu.
        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("theme-toggle")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.setFixedSize(28, 24)
        self.theme_btn.clicked.connect(self._toggle_theme)
        mb.setCornerWidget(self.theme_btn, Qt.Corner.TopRightCorner)

    def _set_workers(self, n):
        self._max_workers = n
        for num, act in self._workers_actions:
            act.setChecked(num == n)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(14, 12, 14, 12)
        main_layout.setSpacing(10)

        # -------------------------------------------------------------------
        # 1. Top Section: Input / Output & Media Info
        # -------------------------------------------------------------------
        io_card = QFrame()
        io_card.setObjectName("header-card")
        io_layout = QVBoxLayout(io_card)
        io_layout.setContentsMargins(12, 10, 12, 10)
        io_layout.setSpacing(8)

        # Title
        t_lbl = QLabel("INPUT & OUTPUT SOURCES")
        t_lbl.setObjectName("section-title")
        io_layout.addWidget(t_lbl)

        # Input Row
        in_row = QHBoxLayout()
        in_row.addWidget(QLabel("Input:"))
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("Select a video file or folder containing videos…")
        self.input_edit.textChanged.connect(self._on_input_changed)
        in_row.addWidget(self.input_edit, 1)

        btn_file = QPushButton("Browse File")
        btn_file.setObjectName("btn-primary")
        btn_file.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_file.clicked.connect(self._pick_file)
        in_row.addWidget(btn_file)

        btn_dir = QPushButton("Browse Folder")
        btn_dir.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_dir.clicked.connect(self._pick_input_dir)
        in_row.addWidget(btn_dir)
        io_layout.addLayout(in_row)

        # Output Row
        out_row = QHBoxLayout()
        out_row.addWidget(QLabel("Output:"))
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText("Output directory (defaults to input location)…")
        out_row.addWidget(self.output_edit, 1)

        btn_out = QPushButton("Select Folder")
        btn_out.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_out.clicked.connect(self._pick_output_dir)
        out_row.addWidget(btn_out)
        io_layout.addLayout(out_row)

        # Compact Info Bar
        self.info_label = QLabel("No video selected")
        io_layout.addWidget(self.info_label)

        main_layout.addWidget(io_card)

        # -------------------------------------------------------------------
        # 2. Main 2-Column Options Grid
        # -------------------------------------------------------------------
        cols_layout = QHBoxLayout()
        cols_layout.setSpacing(10)

        # --- LEFT COLUMN: Frame Selection & Filters ---
        left_card = QFrame()
        left_card.setObjectName("card")
        left_layout = QVBoxLayout(left_card)
        left_layout.setContentsMargins(12, 10, 12, 12)
        left_layout.setSpacing(10)

        l_title = QLabel("FRAME FILTERING & EXTRACTION")
        l_title.setObjectName("section-title")
        left_layout.addWidget(l_title)

        form_l = QFormLayout()
        form_l.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_l.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_l.setHorizontalSpacing(12)
        form_l.setVerticalSpacing(8)

        # Step
        self.frame_step = QSpinBox()
        self.frame_step.setRange(1, 10000)
        self.frame_step.setValue(1)
        self.frame_step.setFixedWidth(100)
        self.frame_step.setCursor(Qt.CursorShape.PointingHandCursor)
        form_l.addRow(
            self._field_label(
                "Frame Step (Interval):",
                "Extract every Nth frame. 1 = every frame, 5 = every 5th frame. "
                "Higher values mean fewer, more spread-out images.",
            ),
            self.frame_step,
        )

        # Start / End Time
        time_box = QHBoxLayout()
        self.start_time = QDoubleSpinBox()
        self.start_time.setRange(0, 999999)
        self.start_time.setDecimals(1)
        self.start_time.setSpecialValueText("Start")
        self.start_time.setFixedWidth(85)

        self.end_time = QDoubleSpinBox()
        self.end_time.setRange(0, 999999)
        self.end_time.setDecimals(1)
        self.end_time.setSpecialValueText("End")
        self.end_time.setFixedWidth(85)

        time_box.addWidget(self.start_time)
        time_box.addWidget(QLabel("to"))
        time_box.addWidget(self.end_time)
        time_box.addStretch()
        form_l.addRow(
            self._field_label(
                "Time Range (sec):",
                "Only extract frames between these two timestamps, in seconds. "
                "Leave both as Start/End to use the whole video.",
            ),
            time_box,
        )

        # Range
        self.frame_range_edit = QLineEdit()
        self.frame_range_edit.setPlaceholderText("e.g. 100-500")
        self.frame_range_edit.setFixedWidth(180)
        form_l.addRow(
            self._field_label(
                "Frame Index Range:",
                "Only extract frames whose index falls in this range, e.g. 100-500. "
                "Leave blank to use every frame.",
            ),
            self.frame_range_edit,
        )

        left_layout.addLayout(form_l)

        # Line Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        left_layout.addWidget(line)

        # Photogrammetry & Smart Filters
        photog_title = QLabel("PHOTOGRAMMETRY & SMART FILTERS")
        photog_title.setObjectName("section-title")
        left_layout.addWidget(photog_title)

        # Quick preset — auto-configures the fields below for common
        # photogrammetry scenarios so new users don't need to hand-tune
        # scene/motion thresholds themselves.
        preset_row = QHBoxLayout()
        preset_row.setSpacing(5)
        preset_row.addWidget(QLabel("Quick Preset:"))
        preset_row.addWidget(
            self._info_icon(
                "Pick a scenario to auto-configure Keyframe Mode, thresholds, and "
                "image format for you. Choose Custom to set every option yourself."
            )
        )
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(list(PHOTOGRAMMETRY_PRESETS.keys()))
        self.preset_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.preset_combo.currentTextChanged.connect(self._on_preset_changed)
        preset_row.addWidget(self.preset_combo, 1)
        left_layout.addLayout(preset_row)

        self.preset_desc = QLabel(PHOTOGRAMMETRY_PRESETS[CUSTOM_PRESET_NAME]["desc"])
        self.preset_desc.setObjectName("preset-desc")
        self.preset_desc.setWordWrap(True)
        left_layout.addWidget(self.preset_desc)

        self.keyframe_check = QCheckBox("Keyframe Mode (Photogrammetry Preset)")
        left_layout.addWidget(
            self._checkbox_row(
                self.keyframe_check,
                "Automatically keeps only visually distinct frames — ideal for 3D "
                "reconstruction (COLMAP, Meshroom, RealityCapture). Overrides Scene "
                "Detection and Duplicate Removal.",
            )
        )

        scene_box = QHBoxLayout()
        self.scene_check = QCheckBox("Scene Change Detection:")
        self.scene_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scene_thresh = QDoubleSpinBox()
        self.scene_thresh.setRange(0, 255)
        self.scene_thresh.setValue(30.0)
        self.scene_thresh.setFixedWidth(70)
        scene_tip = (
            "Skips frames that look almost identical to the previous one. Lower "
            "threshold = more sensitive (keeps more frames); higher = only keeps "
            "frames with a bigger visual change."
        )
        self.scene_check.setToolTip(scene_tip)
        self.scene_thresh.setToolTip(scene_tip)
        scene_box.addWidget(self.scene_check)
        scene_box.addWidget(self.scene_thresh)
        scene_box.addWidget(self._info_icon(scene_tip))
        scene_box.addStretch()
        left_layout.addLayout(scene_box)

        motion_box = QHBoxLayout()
        self.motion_check = QCheckBox("Motion Threshold Filter:")
        self.motion_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.motion_thresh = QDoubleSpinBox()
        self.motion_thresh.setRange(0, 1000)
        self.motion_thresh.setValue(5.0)
        self.motion_thresh.setFixedWidth(70)
        motion_tip = (
            "Skips frames with little camera/subject motion. Raise this if you're "
            "getting too many near-static frames; lower it if slow movement is "
            "being missed."
        )
        self.motion_check.setToolTip(motion_tip)
        self.motion_thresh.setToolTip(motion_tip)
        motion_box.addWidget(self.motion_check)
        motion_box.addWidget(self.motion_thresh)
        motion_box.addWidget(self._info_icon(motion_tip))
        motion_box.addStretch()
        left_layout.addLayout(motion_box)

        self.dedup_check = QCheckBox("Remove Duplicate Frames")
        left_layout.addWidget(
            self._checkbox_row(
                self.dedup_check,
                "Compares a fingerprint of each frame and skips exact repeats — "
                "useful for static shots or paused footage.",
            )
        )

        left_layout.addStretch()
        cols_layout.addWidget(left_card, 1)

        # --- RIGHT COLUMN: Image Output & Naming ---
        right_card = QFrame()
        right_card.setObjectName("card")
        right_layout = QVBoxLayout(right_card)
        right_layout.setContentsMargins(12, 10, 12, 12)
        right_layout.setSpacing(10)

        r_title = QLabel("FORMAT & FILE NAMING")
        r_title.setObjectName("section-title")
        right_layout.addWidget(r_title)

        form_r = QFormLayout()
        form_r.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_r.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        form_r.setHorizontalSpacing(12)
        form_r.setVerticalSpacing(8)

        # Format
        self.format_combo = QComboBox()
        self.format_combo.addItems(["jpg", "png"])
        self.format_combo.setFixedWidth(90)
        self.format_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.format_combo.currentTextChanged.connect(self._on_format_changed)
        form_r.addRow("Image Format:", self.format_combo)

        # JPEG Quality Row
        self.jpeg_label = QLabel("JPEG Quality:")
        self.jpeg_widget = QWidget()
        j_box = QHBoxLayout(self.jpeg_widget)
        j_box.setContentsMargins(0, 0, 0, 0)
        self.jpeg_quality = QSlider(Qt.Orientation.Horizontal)
        self.jpeg_quality.setRange(1, 100)
        self.jpeg_quality.setValue(95)
        self.jpeg_quality.setFixedWidth(120)
        jpeg_tip = "Higher values keep more detail but produce larger files. 90-100 is recommended for photogrammetry."
        self.jpeg_quality.setToolTip(jpeg_tip)
        self.jpeg_qlabel = QLabel("95")
        self.jpeg_qlabel.setFixedWidth(24)
        self.jpeg_quality.valueChanged.connect(lambda v: self.jpeg_qlabel.setText(str(v)))
        j_box.addWidget(self.jpeg_quality)
        j_box.addWidget(self.jpeg_qlabel)
        j_box.addWidget(self._info_icon(jpeg_tip))
        j_box.addStretch()
        form_r.addRow(self.jpeg_label, self.jpeg_widget)

        # PNG Compression Row
        self.png_label = QLabel("PNG Compression:")
        self.png_widget = QWidget()
        p_box = QHBoxLayout(self.png_widget)
        p_box.setContentsMargins(0, 0, 0, 0)
        self.png_compression = QSlider(Qt.Orientation.Horizontal)
        self.png_compression.setRange(0, 9)
        self.png_compression.setValue(6)
        self.png_compression.setFixedWidth(120)
        png_tip = "Controls file size vs. save speed only — PNG is always lossless, so image quality is unaffected."
        self.png_compression.setToolTip(png_tip)
        self.png_clabel = QLabel("6")
        self.png_clabel.setFixedWidth(24)
        self.png_compression.valueChanged.connect(lambda v: self.png_clabel.setText(str(v)))
        p_box.addWidget(self.png_compression)
        p_box.addWidget(self.png_clabel)
        p_box.addWidget(self._info_icon(png_tip))
        p_box.addStretch()
        form_r.addRow(self.png_label, self.png_widget)

        # Initial format visibility
        self._on_format_changed(self.format_combo.currentText())

        # Resize Checkbox & W x H
        self.resize_check = QCheckBox("Enable Frame Resizing")
        self.resize_check.setChecked(False)
        self.resize_check.toggled.connect(self._on_resize_toggled)
        right_layout.addWidget(
            self._checkbox_row(
                self.resize_check,
                "Scale output images down (or up) from the original video resolution. "
                "Leave both fields as Auto to keep the source size.",
            )
        )

        res_box = QHBoxLayout()
        self.resize_w = QSpinBox()
        self.resize_w.setRange(0, 99999)
        self.resize_w.setSpecialValueText("Auto")
        self.resize_w.setFixedWidth(75)
        self.resize_w.setEnabled(False)

        self.resize_h = QSpinBox()
        self.resize_h.setRange(0, 99999)
        self.resize_h.setSpecialValueText("Auto")
        self.resize_h.setFixedWidth(75)
        self.resize_h.setEnabled(False)

        res_box.addWidget(self.resize_w)
        res_box.addWidget(QLabel("×"))
        res_box.addWidget(self.resize_h)
        res_box.addStretch()
        form_r.addRow(
            self._field_label(
                "Resize (W × H):",
                "Set a target width and/or height in pixels. Fill in only one side "
                "to scale proportionally; Auto keeps the original size.",
            ),
            res_box,
        )

        right_layout.addLayout(form_r)

        self.grayscale_check = QCheckBox("Convert to Grayscale")
        right_layout.addWidget(
            self._checkbox_row(
                self.grayscale_check,
                "Saves images in black & white. Rarely used for photogrammetry — "
                "most reconstruction tools expect color.",
            )
        )

        # Line Separator
        line_r = QFrame()
        line_r.setFrameShape(QFrame.Shape.HLine)
        right_layout.addWidget(line_r)

        form_r2 = QFormLayout()
        form_r2.setHorizontalSpacing(12)
        form_r2.setVerticalSpacing(8)

        # Pattern
        self.naming_pattern = QLineEdit()
        self.naming_pattern.setPlaceholderText("{video}_frame_{frame:04d}")
        form_r2.addRow(
            self._field_label(
                "Naming Template:",
                "Customize output filenames with placeholders: {video} = source "
                "filename, {frame:04d} = zero-padded frame number, {time} = "
                "timestamp in seconds, {datetime} = current date/time.",
            ),
            self.naming_pattern,
        )

        # Prefix / Suffix
        ps_box = QHBoxLayout()
        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("Prefix")
        self.suffix_edit = QLineEdit()
        self.suffix_edit.setPlaceholderText("Suffix")
        ps_box.addWidget(self.prefix_edit)
        ps_box.addWidget(self.suffix_edit)
        form_r2.addRow(
            self._field_label(
                "Prefix & Suffix:",
                "Extra text added to the start/end of every filename, before the "
                "file extension. Ignored when a Naming Template is set above.",
            ),
            ps_box,
        )

        right_layout.addLayout(form_r2)

        self.timestamp_check = QCheckBox("Include Timestamp in Filename")
        right_layout.addWidget(
            self._checkbox_row(
                self.timestamp_check,
                "Appends the extraction date & time to every filename — handy for "
                "telling batches apart.",
            )
        )

        self.parent_check = QCheckBox("Include Parent Directory in Output Path")
        right_layout.addWidget(
            self._checkbox_row(
                self.parent_check,
                "Recreates the source video's parent folder name inside the output "
                "directory — useful when batch-processing nested folders.",
            )
        )

        right_layout.addStretch()
        cols_layout.addWidget(right_card, 1)

        main_layout.addLayout(cols_layout, 1)

        # -------------------------------------------------------------------
        # 3. Action Footer & Progress Bar
        # -------------------------------------------------------------------
        action_card = QFrame()
        action_card.setObjectName("card")
        act_layout = QVBoxLayout(action_card)
        act_layout.setContentsMargins(12, 10, 12, 10)
        act_layout.setSpacing(8)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)
        act_layout.addWidget(self.progress_bar)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_start = QPushButton("▶  Start Frame Extraction")
        self.btn_start.setObjectName("btn-start")
        self.btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_start.clicked.connect(self._start)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("btn-cancel")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.clicked.connect(self._cancel)

        btn_row.addWidget(self.btn_start)
        btn_row.addWidget(self.btn_cancel)
        act_layout.addLayout(btn_row)

        main_layout.addWidget(action_card)

    # ---------------------------------------------------------------------------
    # Photogrammetry presets
    # ---------------------------------------------------------------------------
    def _on_preset_changed(self, name):
        preset = PHOTOGRAMMETRY_PRESETS.get(name, PHOTOGRAMMETRY_PRESETS[CUSTOM_PRESET_NAME])
        self.preset_desc.setText(preset["desc"])
        if name == CUSTOM_PRESET_NAME:
            return

        self.keyframe_check.setChecked(preset["keyframe"])
        self.frame_step.setValue(preset["frame_step"])
        self.scene_check.setChecked(True)
        self.scene_thresh.setValue(preset["scene_threshold"])
        self.motion_check.setChecked(True)
        self.motion_thresh.setValue(preset["motion_threshold"])
        self.dedup_check.setChecked(True)
        idx = self.format_combo.findText(preset["format"])
        if idx >= 0:
            self.format_combo.setCurrentIndex(idx)

    # ---------------------------------------------------------------------------
    # File Pickers & Info
    # ---------------------------------------------------------------------------
    def _pick_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            "Video Files (*.mp4 *.mkv *.avi *.mov *.webm *.flv *.wmv);;All Files (*)",
        )
        if path:
            self.input_edit.setText(path)

    def _pick_input_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Video Directory")
        if path:
            self.input_edit.setText(path)

    def _pick_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if path:
            self.output_edit.setText(path)

    def _on_input_changed(self, text):
        path = text.strip()
        if os.path.isfile(path):
            self._show_video_info(path)
        elif os.path.isdir(path):
            videos = []
            for ext in ["*.mp4", "*.mkv", "*.avi", "*.mov", "*.webm", "*.flv", "*.wmv"]:
                videos.extend(glob.glob(os.path.join(path, ext)))
                videos.extend(glob.glob(os.path.join(path, ext.upper())))
            videos = list(set(videos))
            self.info_label.setText(f"📁 Folder Mode: {len(videos)} video file(s) found")
        else:
            self.info_label.setText("No video selected")

    def _show_video_info(self, path):
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            self.info_label.setText("⚠ Could not read video file")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        duration = frames / fps if fps > 0 else 0
        mins, secs = divmod(duration, 60)
        hrs, mins = divmod(int(mins), 60)
        dur_str = f"{int(hrs)}h {int(mins)}m {secs:.1f}s" if hrs else (f"{int(mins)}m {secs:.1f}s" if mins else f"{secs:.1f}s")

        self.info_label.setText(
            f"📹 {os.path.basename(path)}   |   Duration: {dur_str}   |   FPS: {fps:.2f}   |   Total Frames: {frames:,}   |   Resolution: {w}×{h}"
        )

    def _on_format_changed(self, fmt):
        is_png = (fmt.lower() == "png")
        self.jpeg_label.setVisible(not is_png)
        self.jpeg_widget.setVisible(not is_png)
        self.png_label.setVisible(is_png)
        self.png_widget.setVisible(is_png)

    def _on_resize_toggled(self, checked):
        self.resize_w.setEnabled(checked)
        self.resize_h.setEnabled(checked)

    def _collect_kwargs(self):
        use_resize = self.resize_check.isChecked()
        return {
            "include_parent": self.parent_check.isChecked(),
            "image_format": self.format_combo.currentText(),
            "frame_step": self.frame_step.value(),
            "start_time": self.start_time.value() or None,
            "end_time": self.end_time.value() or None,
            "frame_range": self._parse_frame_range(),
            "naming_pattern": self.naming_pattern.text().strip() or None,
            "prefix": self.prefix_edit.text().strip(),
            "suffix": self.suffix_edit.text().strip(),
            "include_timestamp": self.timestamp_check.isChecked(),
            "jpeg_quality": self.jpeg_quality.value(),
            "png_compression": self.png_compression.value(),
            "resize_width": (self.resize_w.value() or None) if use_resize else None,
            "resize_height": (self.resize_h.value() or None) if use_resize else None,
            "grayscale": self.grayscale_check.isChecked(),
            "scene_detection": self.scene_check.isChecked(),
            "scene_threshold": self.scene_thresh.value(),
            "motion_based": self.motion_check.isChecked(),
            "motion_threshold": self.motion_thresh.value(),
            "remove_duplicates": self.dedup_check.isChecked(),
            "keyframe_only": self.keyframe_check.isChecked(),
        }

    def _parse_frame_range(self):
        text = self.frame_range_edit.text().strip()
        if not text:
            return None
        if "-" in text:
            parts = text.split("-")
            try:
                return (int(parts[0]), int(parts[1]))
            except ValueError:
                return None
        try:
            return (int(text), None)
        except ValueError:
            return None

    def _start(self):
        input_path = self.input_edit.text().strip()
        if not input_path:
            QMessageBox.warning(self, "Missing Input", "Please select a video file or folder first.")
            return

        output_path = self.output_edit.text().strip() or (
            os.path.dirname(input_path) if os.path.isfile(input_path) else input_path
        )
        kwargs = self._collect_kwargs()

        is_batch = False
        if os.path.isfile(input_path):
            video_paths = [input_path]
        elif os.path.isdir(input_path):
            is_batch = True
            if self._act_recursive.isChecked():
                video_paths = find_videos_recursive(input_path)
            else:
                video_paths = []
                for ext in ["*.mp4", "*.mkv", "*.avi", "*.mov", "*.MP4", "*.MKV", "*.AVI", "*.MOV", "*.webm", "*.flv", "*.wmv"]:
                    video_paths.extend(glob.glob(os.path.join(input_path, ext)))
            video_paths = list(set(video_paths))
            if not video_paths:
                QMessageBox.warning(self, "No Videos Found", "No supported video files found in the directory.")
                return
            if self._act_parallel.isChecked():
                kwargs["parallel"] = True
                kwargs["max_workers"] = self._max_workers
        else:
            QMessageBox.warning(self, "Invalid Path", "Selected path does not exist.")
            return

        self.btn_start.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setRange(0, 0)
        self.statusBar().showMessage("Extracting frames… Please wait.")

        self.worker = ExtractionWorker(video_paths, output_path, kwargs, is_batch)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_progress(self, current, total):
        if self.progress_bar.maximum() == 0:
            self.progress_bar.setRange(0, max(total, 1))
        self.progress_bar.setValue(current)

    def _cancel(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
            self._reset_ui("Extraction cancelled by user")

    def _on_finished(self, msg):
        self._reset_ui("Extraction complete")
        QMessageBox.information(self, "Done", msg)

    def _on_error(self, msg):
        self._reset_ui("Extraction error")
        QMessageBox.critical(self, "Error", msg)

    def _reset_ui(self, status_msg):
        self.btn_start.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage(status_msg)

    def _show_about(self):
        QMessageBox.about(
            self,
            "About Video2Image",
            f"<h3>Video2Image v{VERSION}</h3>"
            "<p>Photogrammetry-focused video frame extractor.</p>"
            "<p>Designed for 3D reconstruction pipelines (COLMAP, Meshroom, Reality Capture).</p>"
            "<hr>"
            "<p>© 2024 Sakthivel J — <a href='https://github.com/sakthivelj/video2image'>GitHub Repository</a></p>"
            "<p>Contact: <a href='mailto:sakthivel1023@gmail.com'>sakthivel1023@gmail.com</a></p>",
        )

    def _show_tips(self):
        QMessageBox.information(
            self,
            "Photogrammetry Workflow Tips",
            "<h3>🎯 Photogrammetry Frame Extraction Tips</h3>"
            "<ul>"
            "<li><b>Quick Preset:</b> Pick the scenario that matches your footage (aerial, "
            "handheld, turntable) and the thresholds are set for you.</li>"
            "<li><b>Keyframe Mode:</b> Automatically extracts unique, visually distinct frames for 3D reconstruction.</li>"
            "<li><b>Frame Step:</b> Use step 5-10 for walking videos, 2-3 for aerial/drone footage.</li>"
            "<li><b>Format:</b> PNG is recommended for lossless image quality in Meshroom/COLMAP.</li>"
            "<li><b>Resolution:</b> Keep original resolution whenever possible for maximum feature detection.</li>"
            "</ul>",
        )


def _claim_windows_app_id():
    """Give this process its own Application User Model ID.

    Without this, Windows groups the taskbar button under python.exe's own
    identity and shows the Python icon there instead of ours, even though
    the window/title-bar icon is set correctly via setWindowIcon.
    """
    if sys.platform != "win32":
        return
    import ctypes

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            f"{ORG_NAME}.{APP_NAME}.gui"
        )
    except (AttributeError, OSError):
        pass


def main():
    _claim_windows_app_id()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    icon_path = _resource_path("logo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
