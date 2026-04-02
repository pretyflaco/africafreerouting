#!/usr/bin/env python3
"""Generate masterclass presentation slides for Africa Free Routing Lightning Payment Integration.

Day 2: Blink API + AI Coding Tools  —  April 2, 2026, 18:00-20:00 UTC
"""

import os
import subprocess
import tempfile

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(
    TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
)
pdfmetrics.registerFont(
    TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
)
pdfmetrics.registerFont(
    TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
)
pdfmetrics.registerFont(
    TTFont("MonoBold", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")
)

W, H = landscape(A4)
TOTAL_SLIDES = 13

# ─── Paths ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
AFR_LOGO = os.path.join(REPO_ROOT, "africafreerouting", "Africa_Free_Routing_image.png")
BLINK_SVG = os.path.join(REPO_ROOT, "africafreerouting", "Blink logo_white.svg")

# ─── Colors ──────────────────────────────────────────────────────────────
BG = (0.07, 0.07, 0.12)
FG = (0.88, 0.88, 0.92)
GREEN = (0.30, 0.85, 0.55)
CYAN = (0.35, 0.78, 0.95)
YELLOW = (0.95, 0.80, 0.25)
DIM = (0.45, 0.45, 0.55)
ACCENT = (0.55, 0.35, 0.95)
CODE_BG = (0.10, 0.10, 0.16)
ORANGE = (0.95, 0.55, 0.20)
RED = (0.90, 0.30, 0.30)
LIGHTNING = (1.0, 0.72, 0.0)  # Bitcoin orange-gold


# ─── Drawing helpers ─────────────────────────────────────────────────────


def _bg(c):
    c.setFillColorRGB(*BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def _text(c, x, y, txt, font="DejaVu", size=18, color=FG):
    c.setFillColorRGB(*color)
    c.setFont(font, size)
    c.drawString(x, y, txt)


def _text_center(c, y, txt, font="DejaVu", size=18, color=FG):
    c.setFillColorRGB(*color)
    c.setFont(font, size)
    tw = c.stringWidth(txt, font, size)
    c.drawString((W - tw) / 2, y, txt)


def _text_right(c, x, y, txt, font="DejaVu", size=18, color=FG):
    c.setFillColorRGB(*color)
    c.setFont(font, size)
    tw = c.stringWidth(txt, font, size)
    c.drawString(x - tw, y, txt)


def _bullet(c, x, y, txt, size=14, color=FG, bullet_color=GREEN):
    _text(c, x, y, "▸", font="DejaVu", size=size, color=bullet_color)
    _text(c, x + 20, y, txt, font="DejaVu", size=size, color=color)


def _slide_num(c, num):
    _text(c, W - 60, 20, f"{num}/{TOTAL_SLIDES}", font="Mono", size=10, color=DIM)


def _divider(c, y, x1=None, x2=None):
    if x1 is None:
        x1 = W * 0.15
    if x2 is None:
        x2 = W * 0.85
    c.setStrokeColorRGB(*DIM)
    c.setLineWidth(0.5)
    c.line(x1, y, x2, y)


def _code_box(c, x, y, w, h, radius=6):
    c.setFillColorRGB(*CODE_BG)
    c.setStrokeColorRGB(0.25, 0.25, 0.35)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def _pipeline_box(c, x, y, w, h, label, color, desc_lines=None, font_size=11):
    c.setStrokeColorRGB(*color)
    c.setLineWidth(1.5)
    c.setFillColorRGB(*CODE_BG)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=1)
    lines = label.split("\n")
    for j, line in enumerate(lines):
        lw = c.stringWidth(line, "DejaVuBold", font_size)
        _text(
            c,
            x + (w - lw) / 2,
            y + h / 2 + 4 - j * (font_size + 3),
            line,
            font="DejaVuBold",
            size=font_size,
            color=color,
        )
    if desc_lines:
        for j, dl in enumerate(desc_lines):
            dlw = c.stringWidth(dl, "Mono", 8)
            _text(
                c,
                x + (w - dlw) / 2,
                y - 14 - j * 12,
                dl,
                font="Mono",
                size=8,
                color=DIM,
            )


def _arrow_right(c, x, y, length=20):
    c.setStrokeColorRGB(*DIM)
    c.setLineWidth(1)
    c.line(x, y, x + length, y)
    _text(c, x + length - 4, y - 4, "→", font="DejaVu", size=12, color=DIM)


# ─── Logo helpers ────────────────────────────────────────────────────────

_blink_png_path = None


def _get_blink_png():
    global _blink_png_path
    if _blink_png_path and os.path.exists(_blink_png_path):
        return _blink_png_path
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    subprocess.run(
        ["convert", "-background", "none", "-resize", "200x60", BLINK_SVG, path],
        check=True,
        capture_output=True,
    )
    _blink_png_path = path
    return path


def _draw_afr_logo(c, x, y, max_w, max_h):
    """Draw Africa Free Routing logo scaled to fit within max_w x max_h."""
    img = ImageReader(AFR_LOGO)
    iw, ih = img.getSize()
    ratio = min(max_w / iw, max_h / ih)
    dw, dh = iw * ratio, ih * ratio
    c.drawImage(img, x, y, width=dw, height=dh, mask="auto")
    return dw, dh


def _draw_blink_logo(c, x, y, max_w=120, max_h=40):
    """Draw Blink logo scaled to fit."""
    png = _get_blink_png()
    img = ImageReader(png)
    iw, ih = img.getSize()
    ratio = min(max_w / iw, max_h / ih)
    dw, dh = iw * ratio, ih * ratio
    c.drawImage(img, x, y, width=dw, height=dh, mask="auto")
    return dw, dh


def _generate_qr_image(url, box_size=8, border=2):
    """Generate a QR code as a PIL Image."""
    import qrcode

    qr = qrcode.QRCode(
        version=1,
        box_size=box_size,
        border=border,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").get_image()


# ─── Slides ──────────────────────────────────────────────────────────────


def slide_01_title(c):
    """Title slide with logos."""
    _bg(c)

    # Africa Free Routing logo (centered, upper area)
    _draw_afr_logo(c, (W - 280) / 2, H - 220, 280, 160)

    # Main title
    _text_center(
        c,
        H - 260,
        "Lightning Payment Integration Masterclass",
        font="DejaVuBold",
        size=26,
        color=LIGHTNING,
    )

    # Subtitle
    _text_center(
        c,
        H - 300,
        "Day 2: Blink API + AI Coding Tools",
        font="DejaVu",
        size=20,
        color=CYAN,
    )

    _divider(c, H - 330)

    # Date and series
    _text_center(
        c,
        H - 365,
        "April 2, 2026  ·  18:00-20:00 UTC",
        font="DejaVu",
        size=16,
        color=DIM,
    )

    # Instructors
    _text_center(
        c,
        H - 405,
        "Instructors:  @kemal (lead)  ·  @Kim Neunert  ·  @Openoms",
        font="DejaVu",
        size=15,
        color=FG,
    )

    # 3-day series
    _text_center(
        c,
        H - 450,
        "Day 1: MavaPay  ─  Day 2: Blink  ─  Day 3: BTCPay Server",
        font="Mono",
        size=13,
        color=DIM,
    )

    # Blink logo bottom-right
    _draw_blink_logo(c, W - 160, 25, max_w=120, max_h=35)

    # Repo
    _text(
        c,
        40,
        30,
        "github.com/pretyflaco/africafreerouting",
        font="Mono",
        size=11,
        color=DIM,
    )

    _slide_num(c, 1)
    c.showPage()


def slide_02_series(c):
    """3-Day Series context."""
    _bg(c)
    _text(
        c,
        60,
        H - 80,
        "3-Day Masterclass Series",
        font="DejaVuBold",
        size=32,
        color=GREEN,
    )

    _text_center(
        c,
        H - 140,
        "Lightning Payment Integration for Africa",
        font="DejaVu",
        size=18,
        color=DIM,
    )

    # Three day boxes
    days = [
        ("Day 1", "MavaPay / V2Pay", "Mobile money\nintegration", DIM),
        ("Day 2", "Blink", "API + AI coding\ntools", LIGHTNING),
        ("Day 3", "BTCPay Server", "Self-hosted\npayment server", DIM),
    ]
    box_w, box_h = 210, 120
    gap = 40
    total_w = len(days) * box_w + (len(days) - 1) * gap
    start_x = (W - total_w) / 2
    y_box = H - 320

    for i, (day, name, desc, color) in enumerate(days):
        x = start_x + i * (box_w + gap)
        is_active = i == 1
        border_color = LIGHTNING if is_active else DIM
        lw = 3 if is_active else 1
        c.setStrokeColorRGB(*border_color)
        c.setLineWidth(lw)
        c.setFillColorRGB(*(0.12, 0.12, 0.18) if is_active else CODE_BG)
        c.roundRect(x, y_box, box_w, box_h, 8, fill=1, stroke=1)
        _text(
            c,
            x + 15,
            y_box + box_h - 28,
            day,
            font="MonoBold",
            size=14,
            color=border_color,
        )
        _text(
            c,
            x + 15,
            y_box + box_h - 52,
            name,
            font="DejaVuBold",
            size=18,
            color=FG if is_active else DIM,
        )
        for j, dl in enumerate(desc.split("\n")):
            _text(c, x + 15, y_box + 22 - j * 14, dl, font="Mono", size=10, color=DIM)

        # Arrow between boxes
        if i < len(days) - 1:
            ax = x + box_w + 5
            c.setStrokeColorRGB(*DIM)
            c.setLineWidth(1)
            mid_y = y_box + box_h / 2
            c.line(ax, mid_y, ax + gap - 10, mid_y)
            _text(c, ax + gap - 14, mid_y - 5, "→", font="DejaVu", size=14, color=DIM)

    # Audience info
    y = y_box - 60
    _text_center(
        c,
        y,
        "100+ participants from across Africa",
        font="DejaVuBold",
        size=20,
        color=FG,
    )
    _text_center(
        c,
        y - 35,
        "Developers  ·  Entrepreneurs  ·  Educators",
        font="DejaVu",
        size=17,
        color=CYAN,
    )

    _text_center(
        c,
        60,
        '"Move participants from curiosity to real implementation"',
        font="DejaVu",
        size=14,
        color=DIM,
    )

    _slide_num(c, 2)
    c.showPage()


def slide_03_what_we_build(c):
    """What We'll Build."""
    _bg(c)
    _text(c, 60, H - 80, "What We'll Build", font="DejaVuBold", size=32, color=GREEN)

    # Big statement
    _text_center(
        c,
        H - 150,
        "A static website that generates Lightning invoices",
        font="DejaVuBold",
        size=22,
        color=LIGHTNING,
    )

    # Feature list
    features = [
        ("BOLT11 invoice generation", "via Blink GraphQL API (no auth)"),
        ("QR code display", "scan with any Lightning wallet"),
        ("Copy invoice button", "for manual paste into wallet"),
        ("Payment detection", "automatic polling every 3 seconds"),
        ("Success animation", "visual confirmation when paid"),
        ("GitHub Pages hosting", "free, no server required"),
    ]
    y = H - 210
    for feat, desc in features:
        _text(c, 100, y, "⚡", font="DejaVu", size=14, color=LIGHTNING)
        _text(c, 125, y, feat, font="DejaVuBold", size=14, color=FG)
        _text(c, 380, y, desc, font="Mono", size=11, color=DIM)
        y -= 30

    _divider(c, y - 10)

    # Big takeaway
    _text_center(
        c,
        y - 50,
        "No server.  No API key.  No cost.",
        font="DejaVuBold",
        size=28,
        color=GREEN,
    )

    # Reference
    _text_center(
        c,
        60,
        "Live demo:  pretyflaco.github.io/africafreerouting",
        font="Mono",
        size=13,
        color=DIM,
    )

    _slide_num(c, 3)
    c.showPage()


def slide_04_toolbox(c):
    """The Toolbox - pipeline diagram."""
    _bg(c)
    _text(c, 60, H - 80, "The Toolbox", font="DejaVuBold", size=32, color=GREEN)

    # Pipeline boxes
    pipeline = [
        ("Terminal", CYAN, ["Linux / macOS / WSL"]),
        ("GitHub\nCLI", GREEN, ["gh repo create", "gh api ..."]),
        ("OpenCode", ACCENT, ["AI coding agent", "in your terminal"]),
        ("LLM", LIGHTNING, ["MiniMax M2.5", "via PPQ.ai"]),
        ("GitHub\nPages", CYAN, ["Free static", "hosting"]),
    ]
    box_w, box_h = 120, 55
    total = len(pipeline)
    gap = (W - 80 - total * box_w) / (total - 1)
    start_x = 40
    y_center = H - 210

    for i, (label, color, desc) in enumerate(pipeline):
        x = start_x + i * (box_w + gap)
        _pipeline_box(c, x, y_center - box_h / 2, box_w, box_h, label, color, desc)
        if i < total - 1:
            ax = x + box_w + 4
            _arrow_right(c, ax, y_center, length=gap - 8)

    # Cost comparison box
    cost_y = H - 370
    _code_box(c, 60, cost_y, W - 120, 80)
    _text(
        c, 80, cost_y + 55, "Cost Comparison", font="DejaVuBold", size=16, color=YELLOW
    )
    _text(
        c,
        80,
        cost_y + 28,
        "MiniMax M2.5:  ~$0.30 / session",
        font="Mono",
        size=13,
        color=GREEN,
    )
    _text(
        c,
        80,
        cost_y + 8,
        "Claude Opus:   ~$25.00 / session",
        font="Mono",
        size=13,
        color=RED,
    )
    _text(
        c,
        480,
        cost_y + 28,
        "PPQ.ai: top up with Lightning",
        font="Mono",
        size=13,
        color=LIGHTNING,
    )
    _text(c, 480, cost_y + 8, "No subscription needed", font="Mono", size=13, color=DIM)

    # Chrome DevTools MCP callout
    y = cost_y - 40
    _text(c, 80, y, "⚡ Chrome DevTools MCP", font="DejaVuBold", size=15, color=CYAN)
    _text(
        c,
        330,
        y,
        "— agent drives the browser, clicks buttons, takes screenshots",
        font="DejaVu",
        size=13,
        color=DIM,
    )

    _slide_num(c, 4)
    c.showPage()


def slide_05_why_lightning(c):
    """Why Lightning for Africa?"""
    _bg(c)
    _text(
        c,
        60,
        H - 80,
        "Why Lightning for Africa?",
        font="DejaVuBold",
        size=32,
        color=GREEN,
    )

    _text_center(c, H - 130, "⚡", font="DejaVu", size=40, color=LIGHTNING)

    points = [
        (
            "No bank account needed",
            "1.4 billion unbanked adults globally, majority in Africa",
        ),
        ("Instant settlement", "Payments confirmed in seconds, not days"),
        (
            "Micro-transactions viable",
            "Send 10 sats ($0.001) — impossible with traditional rails",
        ),
        (
            "Cross-border without friction",
            "No SWIFT, no correspondent banks, no 3-5 business days",
        ),
        ("Growing adoption", "Nigeria, Kenya, Ghana, South Africa leading the way"),
        ("Open infrastructure", "Anyone can build on it — no permission needed"),
        (
            "AI + Lightning",
            "Top up AI tools with sats, monetize apps with micro-payments",
        ),
    ]
    y = H - 190
    for title, desc in points:
        _text(c, 100, y, "⚡", font="DejaVu", size=14, color=LIGHTNING)
        _text(c, 125, y, title, font="DejaVuBold", size=15, color=FG)
        _text(c, 125, y - 18, desc, font="Mono", size=10, color=DIM)
        y -= 48

    _text_center(
        c,
        55,
        '"The internet of money should be as borderless as the internet of information."',
        font="DejaVu",
        size=13,
        color=DIM,
    )

    _slide_num(c, 5)
    c.showPage()


def slide_06_blink_api(c):
    """The Blink API (No Auth) — 2-step flow."""
    _bg(c)
    _text(
        c,
        60,
        H - 80,
        "The Blink API (No Auth Required)",
        font="DejaVuBold",
        size=32,
        color=GREEN,
    )

    _text_center(
        c,
        H - 125,
        "2-step flow to generate a Lightning invoice without any API key",
        font="DejaVu",
        size=16,
        color=DIM,
    )

    # Step 1 box
    s1_x, s1_y, s1_w, s1_h = 50, H - 300, 340, 130
    _code_box(c, s1_x, s1_y, s1_w, s1_h, radius=8)
    _text(
        c,
        s1_x + 15,
        s1_y + s1_h - 25,
        "Step 1: Get Wallet ID",
        font="DejaVuBold",
        size=15,
        color=CYAN,
    )
    code1 = [
        ("query {", GREEN),
        ("  accountDefaultWallet(", FG),
        ('    username: "pretyflaco"', YELLOW),
        ("    walletCurrency: BTC", YELLOW),
        ("  ) { id }", FG),
        ("}", GREEN),
    ]
    cy = s1_y + s1_h - 48
    for line, color in code1:
        _text(c, s1_x + 20, cy, line, font="Mono", size=10, color=color)
        cy -= 14

    # Arrow
    _text(
        c,
        s1_x + s1_w + 15,
        s1_y + s1_h / 2,
        "→  walletId  →",
        font="MonoBold",
        size=14,
        color=LIGHTNING,
    )

    # Step 2 box
    s2_x = s1_x + s1_w + 130
    s2_w = W - s2_x - 50
    _code_box(c, s2_x, s1_y, s2_w, s1_h, radius=8)
    _text(
        c,
        s2_x + 15,
        s1_y + s1_h - 25,
        "Step 2: Create Invoice",
        font="DejaVuBold",
        size=15,
        color=CYAN,
    )
    code2 = [
        ("mutation {", GREEN),
        ("  lnInvoiceCreateOnBehalfOf", FG),
        ("  Recipient(input: {", FG),
        ('    recipientWalletId: "..."', YELLOW),
        ("    amount: 100", YELLOW),
        ("  }) { invoice { paymentRequest } }", FG),
    ]
    cy = s1_y + s1_h - 48
    for line, color in code2:
        _text(c, s2_x + 15, cy, line, font="Mono", size=9, color=color)
        cy -= 14

    # Result
    res_y = s1_y - 50
    _text_center(
        c,
        res_y,
        "→  BOLT11 invoice (lnbc1...)  →  QR code  →  Payment!",
        font="DejaVuBold",
        size=16,
        color=GREEN,
    )

    # Key point
    _code_box(c, 80, res_y - 70, W - 160, 40)
    _text_center(
        c,
        res_y - 55,
        "No API key needed  ·  No authentication  ·  Works from any static website",
        font="DejaVuBold",
        size=14,
        color=LIGHTNING,
    )

    # References
    _text(
        c, 80, 60, "dev.blink.sv/api/agent-playbook", font="Mono", size=11, color=CYAN
    )
    _text(
        c,
        480,
        60,
        "dev.blink.sv/api/no-api-key-operations",
        font="Mono",
        size=11,
        color=CYAN,
    )

    _draw_blink_logo(c, W - 160, 20, max_w=100, max_h=30)

    _slide_num(c, 6)
    c.showPage()


def slide_07_prompt_strategy(c):
    """The Prompt Strategy — sequential steps."""
    _bg(c)
    _text(c, 60, H - 80, "The Prompt Strategy", font="DejaVuBold", size=32, color=GREEN)

    _text_center(
        c,
        H - 125,
        "Small prompts > mega prompts",
        font="DejaVuBold",
        size=20,
        color=YELLOW,
    )
    _text_center(
        c,
        H - 150,
        "Better for learning AND for the AI",
        font="DejaVu",
        size=14,
        color=DIM,
    )

    steps = [
        (
            "1",
            "Create repo + scaffold HTML",
            "gh repo create, index.html, enable GitHub Pages",
            CYAN,
        ),
        (
            "2",
            "Integrate Blink API",
            "Point to dev.blink.sv, discover 2-step flow",
            LIGHTNING,
        ),
        ("3", "Add QR code display", "qrcodejs library, copy button", GREEN),
        (
            "4",
            "Add payment polling",
            "lnInvoicePaymentStatusByPaymentRequest, 3s interval",
            ACCENT,
        ),
        ("5", "Deploy & test live", "Push to GitHub, test payment end-to-end", GREEN),
    ]

    start_y = H - 210
    step_h = 55
    for i, (num, title, desc, color) in enumerate(steps):
        y = start_y - i * (step_h + 8)

        # Step number circle
        cx, cy_c = 100, y + step_h / 2
        c.setFillColorRGB(*color)
        c.circle(cx, cy_c, 18, fill=1, stroke=0)
        _text(c, cx - 5, cy_c - 6, num, font="DejaVuBold", size=16, color=BG)

        # Step content
        _text(c, 135, y + step_h - 18, title, font="DejaVuBold", size=16, color=FG)
        _text(c, 135, y + 8, desc, font="Mono", size=11, color=DIM)

        # Connecting line
        if i < len(steps) - 1:
            c.setStrokeColorRGB(*DIM)
            c.setLineWidth(1)
            c.line(cx, y, cx, y - 8)

    # Bottom note
    _text_center(
        c,
        55,
        "Each prompt = a teaching moment. Pause, explain, discuss.",
        font="DejaVu",
        size=14,
        color=DIM,
    )

    _slide_num(c, 7)
    c.showPage()


def slide_08_payment_flow(c):
    """Payment Flow diagram."""
    _bg(c)
    _text(c, 60, H - 80, "Payment Flow", font="DejaVuBold", size=32, color=GREEN)

    # Flow boxes
    flow = [
        ("User scans\nQR code", CYAN),
        ("Pays\ninvoice", LIGHTNING),
        ("Blink\nnetwork", GREEN),
        ("Poll status\nevery 3s", ACCENT),
        ("PAID ✓", GREEN),
    ]
    box_w, box_h = 130, 60
    total = len(flow)
    gap = (W - 100 - total * box_w) / (total - 1)
    start_x = 50
    y_center = H - 220

    for i, (label, color) in enumerate(flow):
        x = start_x + i * (box_w + gap)
        _pipeline_box(
            c, x, y_center - box_h / 2, box_w, box_h, label, color, font_size=12
        )
        if i < total - 1:
            ax = x + box_w + 4
            _arrow_right(c, ax, y_center, length=gap - 8)

    # Polling detail box
    poll_y = H - 360
    _code_box(c, 60, poll_y, W - 120, 80)
    _text(
        c,
        80,
        poll_y + 55,
        "Payment Status Query (no auth)",
        font="DejaVuBold",
        size=14,
        color=CYAN,
    )
    poll_code = [
        'lnInvoicePaymentStatusByPaymentRequest(input: { paymentRequest: "lnbc1..." })',
        '→ status: "PENDING" | "PAID" | "EXPIRED"',
    ]
    for j, line in enumerate(poll_code):
        _text(c, 80, poll_y + 30 - j * 18, line, font="Mono", size=11, color=FG)

    # WebSocket note
    ws_y = poll_y - 50
    _text(c, 80, ws_y, "Note:", font="DejaVuBold", size=14, color=YELLOW)
    _text(
        c,
        140,
        ws_y,
        "WebSocket subscription exists (wss://ws.blink.sv/graphql)",
        font="DejaVu",
        size=13,
        color=FG,
    )
    _text(
        c,
        80,
        ws_y - 22,
        "but requires authentication. Polling is the no-auth alternative.",
        font="DejaVu",
        size=13,
        color=DIM,
    )

    _slide_num(c, 8)
    c.showPage()


def slide_09_what_can_go_wrong(c):
    """What Can Go Wrong — agent failure modes."""
    _bg(c)
    _text(c, 60, H - 80, "What Can Go Wrong", font="DejaVuBold", size=32, color=GREEN)

    _text_center(
        c,
        H - 125,
        "Common AI agent failure modes (and how to handle them)",
        font="DejaVu",
        size=16,
        color=DIM,
    )

    failures = [
        (
            "❌",
            "Uses authenticated endpoints",
            'Tell it: "Use no-auth endpoints only. Read dev.blink.sv/api/no-api-key-operations"',
            RED,
        ),
        (
            "❌",
            "Does generic web search instead of reading docs",
            "Give it the URL directly. Consider using an OpenCode skill for focused context.",
            RED,
        ),
        (
            "❌",
            "Acts without permission in plan mode",
            "A known issue with some models. Explain it to the audience — awareness matters.",
            RED,
        ),
        (
            "❌",
            "Hallucates API names or parameters",
            'Ask it to test itself: "Can you verify this with curl?" — close the loop.',
            RED,
        ),
        (
            "❌",
            "Goes on a tangent / over-engineers",
            "Interrupt early. Smaller prompts prevent derailing. Restart if needed.",
            RED,
        ),
    ]

    y = H - 180
    for icon, title, fix, color in failures:
        _text(c, 70, y, icon, font="DejaVu", size=16, color=color)
        _text(c, 100, y, title, font="DejaVuBold", size=15, color=FG)
        _text(c, 100, y - 20, fix, font="Mono", size=10, color=DIM)
        y -= 60

    # Big takeaway
    _divider(c, y + 10)
    _text_center(
        c,
        y - 20,
        '"Failure is the best teacher."',
        font="DejaVuBold",
        size=22,
        color=YELLOW,
    )
    _text_center(
        c,
        y - 50,
        "Show failures live — it's more educational than a perfect demo.",
        font="DejaVu",
        size=14,
        color=DIM,
    )

    _slide_num(c, 9)
    c.showPage()


def slide_10_frontend_vs_backend(c):
    """Frontend vs. Backend comparison."""
    _bg(c)
    _text(
        c, 60, H - 80, "Frontend vs. Backend", font="DejaVuBold", size=32, color=GREEN
    )

    col_w = (W - 140) / 2
    col_h = 280
    col_y = H - 120 - col_h
    col1_x = 50
    col2_x = col1_x + col_w + 40

    # Frontend column
    c.setFillColorRGB(*CODE_BG)
    c.setStrokeColorRGB(*CYAN)
    c.setLineWidth(2)
    c.roundRect(col1_x, col_y, col_w, col_h, 8, fill=1, stroke=1)
    _text(
        c,
        col1_x + 20,
        col_y + col_h - 30,
        "Frontend (GitHub Pages)",
        font="DejaVuBold",
        size=18,
        color=CYAN,
    )

    fe_items = [
        ("Free hosting", GREEN),
        ("Static HTML/JS only", FG),
        ("No secrets exposed", FG),
        ("Donation button ✓", GREEN),
        ("QR code display ✓", GREEN),
        ("Invoice generation ✓", GREEN),
        ("Payment polling ✓", GREEN),
    ]
    fy = col_y + col_h - 60
    for item, color in fe_items:
        _bullet(c, col1_x + 25, fy, item, size=13, color=color, bullet_color=CYAN)
        fy -= 28

    _text(c, col1_x + 25, fy, "$0 / month", font="DejaVuBold", size=16, color=GREEN)

    # Backend column
    c.setFillColorRGB(*CODE_BG)
    c.setStrokeColorRGB(*ORANGE)
    c.setLineWidth(2)
    c.roundRect(col2_x, col_y, col_w, col_h, 8, fill=1, stroke=1)
    _text(
        c,
        col2_x + 20,
        col_y + col_h - 30,
        "Backend (VPS / CF Workers)",
        font="DejaVuBold",
        size=18,
        color=ORANGE,
    )

    be_items = [
        ("API keys stay safe", FG),
        ("Check account balance", FG),
        ("Fundraising thermometer", FG),
        ("Webhooks & notifications", FG),
        ("Store state / database", FG),
        ("ntfy.sh push alerts", FG),
    ]
    by = col_y + col_h - 60
    for item, color in be_items:
        _bullet(c, col2_x + 25, by, item, size=13, color=color, bullet_color=ORANGE)
        by -= 28

    _text(
        c,
        col2_x + 25,
        by,
        "~$5 / month (LNVPS or CF Workers)",
        font="DejaVuBold",
        size=13,
        color=ORANGE,
    )

    # Big takeaway
    _text_center(
        c,
        col_y - 40,
        "Start frontend.  Add backend when you need it.",
        font="DejaVuBold",
        size=22,
        color=YELLOW,
    )

    _slide_num(c, 10)
    c.showPage()


def slide_11_poc_to_mvp(c):
    """POC → MVP staircase."""
    _bg(c)
    _text(c, 60, H - 80, "From POC to MVP", font="DejaVuBold", size=32, color=GREEN)

    # Staircase steps
    stairs = [
        (
            "Spike",
            "Can we do it?",
            "Quick experiment to answer\na technical question",
            DIM,
        ),
        (
            "POC",
            "It works!",
            "Demonstrates the concept\nis feasible ← WE ARE HERE",
            CYAN,
        ),
        (
            "Prototype",
            "Users can try it",
            "More complete version\nfor user feedback",
            ACCENT,
        ),
        ("MVP", "Ship it!", "Minimum viable product\nreal users, real value", GREEN),
    ]

    step_w = 160
    step_h = 70
    start_x = 80
    base_y = 130

    for i, (name, tagline, desc, color) in enumerate(stairs):
        x = start_x + i * (step_w + 20)
        y = base_y + i * 55

        # Step box
        c.setFillColorRGB(*CODE_BG)
        c.setStrokeColorRGB(*color)
        lw = 3 if i == 1 else 1.5  # Highlight POC
        c.setLineWidth(lw)
        c.roundRect(x, y, step_w, step_h, 6, fill=1, stroke=1)

        _text(c, x + 12, y + step_h - 22, name, font="DejaVuBold", size=18, color=color)
        _text(c, x + 12, y + step_h - 42, tagline, font="DejaVu", size=12, color=YELLOW)

        # Description below
        for j, dl in enumerate(desc.split("\n")):
            _text(c, x + 12, y - 16 - j * 14, dl, font="Mono", size=9, color=DIM)

        # Arrow
        if i < len(stairs) - 1:
            ax = x + step_w + 2
            ay = y + step_h / 2 + 20
            _text(c, ax, ay, "→", font="DejaVuBold", size=16, color=DIM)

    # Big question
    _text_center(
        c,
        H - 140,
        "Today we built a POC.  What's YOUR next step?",
        font="DejaVuBold",
        size=22,
        color=YELLOW,
    )

    _text_center(
        c,
        H - 175,
        "Don't over-engineer. Use AI to validate fast, then iterate.",
        font="DejaVu",
        size=14,
        color=DIM,
    )

    _slide_num(c, 11)
    c.showPage()


def slide_12_building_blocks(c):
    """Building Blocks — free tools grid."""
    _bg(c)
    _text(c, 60, H - 80, "Building Blocks", font="DejaVuBold", size=32, color=GREEN)

    blocks = [
        (
            "ntfy.sh",
            "Push notifications",
            "Free, no signup, no API key\nSend payment alerts to phone",
            CYAN,
        ),
        (
            "GitHub Pages",
            "Free hosting",
            "Static sites, custom domains\nDeploy with git push",
            GREEN,
        ),
        (
            "Blink API",
            "Lightning invoices",
            "No-auth endpoints available\nGraphQL, well-documented",
            LIGHTNING,
        ),
        (
            "PPQ.ai + ⚡",
            "Cheap AI access",
            "Top up with Lightning\nMiniMax M2.5: ~$0.30/session",
            ACCENT,
        ),
        (
            "Cloudflare Workers",
            "Serverless backend",
            "Free tier: 100K req/day\nNo server to manage",
            ORANGE,
        ),
        (
            "OpenCode",
            "AI coding agent",
            "Terminal-based, open source\nWorks with any LLM provider",
            CYAN,
        ),
    ]

    cols = 3
    rows = 2
    box_w = (W - 140) / cols
    box_h = 110
    gap_x = 20
    gap_y = 20
    start_x = 50
    start_y = H - 150

    for i, (name, subtitle, desc, color) in enumerate(blocks):
        col = i % cols
        row = i // cols
        x = start_x + col * (box_w + gap_x)
        y = start_y - row * (box_h + gap_y) - box_h

        c.setFillColorRGB(*CODE_BG)
        c.setStrokeColorRGB(*color)
        c.setLineWidth(1.5)
        c.roundRect(x, y, box_w, box_h, 6, fill=1, stroke=1)

        _text(c, x + 15, y + box_h - 25, name, font="DejaVuBold", size=16, color=color)
        _text(c, x + 15, y + box_h - 45, subtitle, font="DejaVu", size=12, color=FG)
        for j, dl in enumerate(desc.split("\n")):
            _text(
                c, x + 15, y + box_h - 65 - j * 14, dl, font="Mono", size=9, color=DIM
            )

    # Big takeaway
    _text_center(
        c,
        60,
        "You can build a real product for < $5 / month",
        font="DejaVuBold",
        size=22,
        color=YELLOW,
    )

    _slide_num(c, 12)
    c.showPage()


def slide_13_resources(c):
    """Resources + Questions — closing slide with QR code."""
    _bg(c)

    # Logos at top
    _draw_afr_logo(c, 40, H - 110, 180, 90)
    _draw_blink_logo(c, W - 180, H - 90, max_w=140, max_h=45)

    _text_center(
        c, H - 130, "Resources & Next Steps", font="DejaVuBold", size=30, color=GREEN
    )

    # QR code (left side)
    qr_size = 160
    qr_x = 80
    qr_y = H - 350
    try:
        qr_img = _generate_qr_image("https://github.com/pretyflaco/africafreerouting")
        c.drawImage(ImageReader(qr_img), qr_x, qr_y, width=qr_size, height=qr_size)
    except Exception:
        # Fallback: draw a placeholder box
        c.setStrokeColorRGB(*DIM)
        c.setLineWidth(1)
        c.roundRect(qr_x, qr_y, qr_size, qr_size, 8, fill=0, stroke=1)
        _text(
            c,
            qr_x + 30,
            qr_y + qr_size / 2,
            "[QR Code]",
            font="Mono",
            size=14,
            color=DIM,
        )

    _text(
        c, qr_x, qr_y - 20, "Scan to open the repo", font="DejaVu", size=12, color=DIM
    )

    # Resource list (right side)
    res_x = qr_x + qr_size + 60
    resources = [
        ("Source Code", "github.com/pretyflaco/africafreerouting", CYAN),
        ("Live Demo", "pretyflaco.github.io/africafreerouting", GREEN),
        ("Blink API Playbook", "dev.blink.sv/api/agent-playbook", LIGHTNING),
        ("No-Auth Endpoints", "dev.blink.sv/api/no-api-key-operations", LIGHTNING),
        ("PPQ.ai", "ppq.ai (top up with Lightning)", ACCENT),
        ("OpenCode", "opencode.ai", CYAN),
        ("ntfy.sh", "ntfy.sh (free push notifications)", GREEN),
        ("Blink Dashboard", "dashboard.blink.sv", LIGHTNING),
    ]
    ry = H - 170
    for name, url, color in resources:
        _text(c, res_x, ry, name, font="DejaVuBold", size=13, color=color)
        _text(c, res_x + 180, ry, url, font="Mono", size=10, color=DIM)
        ry -= 24

    # Big "Questions?"
    _text_center(c, 90, "Questions?", font="DejaVuBold", size=40, color=GREEN)
    _text_center(c, 55, "⚡", font="DejaVu", size=24, color=LIGHTNING)

    _text_center(
        c, 25, "@kemal  ·  @Kim Neunert  ·  @Openoms", font="DejaVu", size=13, color=DIM
    )

    _slide_num(c, 13)
    c.showPage()


# ─── Generate ────────────────────────────────────────────────────────────


def generate(output_path):
    c = canvas.Canvas(output_path, pagesize=landscape(A4))
    c.setTitle("Lightning Payment Integration Masterclass — Day 2: Blink")
    c.setAuthor("@kemal · @Kim Neunert · @Openoms")

    slide_01_title(c)
    slide_02_series(c)
    slide_03_what_we_build(c)
    slide_04_toolbox(c)
    slide_05_why_lightning(c)
    slide_06_blink_api(c)
    slide_07_prompt_strategy(c)
    slide_08_payment_flow(c)
    slide_09_what_can_go_wrong(c)
    slide_10_frontend_vs_backend(c)
    slide_11_poc_to_mvp(c)
    slide_12_building_blocks(c)
    slide_13_resources(c)

    c.save()
    print(f"Generated: {output_path} ({TOTAL_SLIDES} slides)")


if __name__ == "__main__":
    out = os.path.join(SCRIPT_DIR, "masterclass_slides.pdf")
    generate(out)
