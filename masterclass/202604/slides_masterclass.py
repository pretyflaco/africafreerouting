#!/usr/bin/env python3
"""Generate masterclass presentation slides for Africa Free Routing Lightning Payment Integration."""

import subprocess
import tempfile
import os

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("MonoBold", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"))

W, H = landscape(A4)

# ─── Paths ───────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_AFR = os.path.join(SCRIPT_DIR, "..", "..", "africafreerouting", "Africa_Free_Routing_image.png")
LOGO_BLINK_SVG = os.path.join(SCRIPT_DIR, "..", "..", "africafreerouting", "Blink logo_white.svg")
OUTPUT = os.path.join(SCRIPT_DIR, "masterclass_slides.pdf")

# ─── Colors ──────────────────────────────────────────────────────────────
BG      = (0.07, 0.07, 0.12)
FG      = (0.88, 0.88, 0.92)
GREEN   = (0.30, 0.85, 0.55)
CYAN    = (0.35, 0.78, 0.95)
YELLOW  = (0.95, 0.80, 0.25)
DIM     = (0.45, 0.45, 0.55)
ACCENT  = (0.55, 0.35, 0.95)
CODE_BG = (0.10, 0.10, 0.16)
ORANGE  = (0.95, 0.55, 0.20)
RED     = (0.90, 0.30, 0.30)
GOLD    = (1.0, 0.72, 0.0)

TOTAL_SLIDES = 13


# ─── Helpers ─────────────────────────────────────────────────────────────

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

def _title(c, txt, color=GREEN):
    _text(c, 60, H - 80, txt, font="DejaVuBold", size=32, color=color)

def _box(c, x, y, w, h, border_color=DIM, fill_color=CODE_BG, radius=6):
    c.setFillColorRGB(*fill_color)
    c.setStrokeColorRGB(*border_color)
    c.setLineWidth(1.5)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)

def _convert_blink_svg():
    """Convert Blink SVG logo to a temp PNG file."""
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp.close()
    try:
        subprocess.run(
            ["convert", "-background", "none", "-density", "150",
             LOGO_BLINK_SVG, tmp.name],
            check=True, capture_output=True
        )
        return tmp.name
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def _draw_logo_afr(c, x, y, max_w, max_h):
    """Draw Africa Free Routing logo scaled to fit."""
    try:
        img = ImageReader(LOGO_AFR)
        iw, ih = img.getSize()
        scale = min(max_w / iw, max_h / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(img, x + (max_w - dw) / 2, y + (max_h - dh) / 2,
                    width=dw, height=dh, mask='auto')
    except Exception:
        _text(c, x + 10, y + max_h / 2, "[Africa Free Routing Logo]", font="DejaVu", size=12, color=DIM)

def _draw_logo_blink(c, blink_png, x, y, max_w, max_h):
    """Draw Blink logo scaled to fit."""
    if blink_png:
        try:
            img = ImageReader(blink_png)
            iw, ih = img.getSize()
            scale = min(max_w / iw, max_h / ih)
            dw, dh = iw * scale, ih * scale
            c.drawImage(img, x + (max_w - dw) / 2, y + (max_h - dh) / 2,
                        width=dw, height=dh, mask='auto')
            return
        except Exception:
            pass
    _text(c, x + 10, y + max_h / 2, "blink", font="DejaVuBold", size=16, color=CYAN)

def _generate_qr_image(url):
    """Generate QR code as PIL Image."""
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image(fill_color="white", back_color="#12121e")
    except ImportError:
        return None


# ─── Slides ──────────────────────────────────────────────────────────────

def slide_01_title(c, blink_png):
    """Title slide with logos."""
    _bg(c)
    # Africa Free Routing logo
    _draw_logo_afr(c, (W - 350) / 2, H - 260, 350, 180)
    # Title
    _text_center(c, H - 300, "Lightning Payment Integration Masterclass",
                 font="DejaVuBold", size=24, color=FG)
    _text_center(c, H - 340, "Day 2: Blink API + AI Coding Tools",
                 font="DejaVu", size=20, color=CYAN)
    # Separator
    c.setStrokeColorRGB(*DIM); c.setLineWidth(0.5)
    c.line(W * 0.25, H - 365, W * 0.75, H - 365)
    # Info
    _text_center(c, H - 400, "April 2, 2026  ·  18:00-20:00 UTC",
                 font="DejaVu", size=14, color=DIM)
    _text_center(c, H - 430, "@pretyflaco  ·  @k9ert (Blink)  ·  @openoms",
                 font="DejaVu", size=14, color=DIM)
    # Blink logo bottom-right
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 1); c.showPage()


def slide_02_series(c, blink_png):
    """3-day series overview."""
    _bg(c)
    _title(c, "3-Day Masterclass Series")
    # Timeline
    days = [
        ("Day 1", "MavaPay / V2Pay", DIM, False),
        ("Day 2", "Blink API", GOLD, True),
        ("Day 3", "BTCPay Server", DIM, False),
    ]
    y_line = H - 220
    x_start, x_end = 120, W - 120
    c.setStrokeColorRGB(*DIM); c.setLineWidth(2)
    c.line(x_start, y_line, x_end, y_line)
    spacing = (x_end - x_start) / 2
    for i, (day, name, color, highlight) in enumerate(days):
        cx = x_start + i * spacing
        if highlight:
            c.setFillColorRGB(*GOLD)
            c.circle(cx, y_line, 10, fill=1)
            _box(c, cx - 90, y_line - 70, 180, 50, border_color=GOLD, fill_color=CODE_BG)
            _text(c, cx - 70, y_line - 38, day, font="DejaVuBold", size=14, color=GOLD)
            _text(c, cx - 70, y_line - 58, name, font="DejaVuBold", size=16, color=GOLD)
        else:
            c.setFillColorRGB(*DIM)
            c.circle(cx, y_line, 6, fill=1)
            _text(c, cx - 40, y_line + 20, day, font="DejaVu", size=12, color=DIM)
            _text(c, cx - 40, y_line - 30, name, font="DejaVu", size=13, color=color)
    # Audience info
    y = H - 360
    _text_center(c, y, "100+ participants from across Africa", font="DejaVuBold", size=22, color=FG)
    y -= 50
    items = [
        ("Developers", "Build Lightning-powered apps", CYAN),
        ("Entrepreneurs", "Integrate payments into businesses", YELLOW),
        ("Educators", "Teach the next generation", GREEN),
    ]
    for label, desc, color in items:
        _text(c, 200, y, "▸", font="DejaVu", size=16, color=color)
        _text(c, 225, y, label, font="DejaVuBold", size=16, color=color)
        _text(c, 400, y, desc, font="DejaVu", size=14, color=DIM)
        y -= 30
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 2); c.showPage()


def slide_03_what_we_build(c, blink_png):
    """What we'll build."""
    _bg(c)
    _title(c, "What We'll Build")
    # Big statement
    _text_center(c, H - 160, "A static website that generates Lightning invoices",
                 font="DejaVuBold", size=22, color=FG)
    _text_center(c, H - 195, "No server. No API key. No cost.",
                 font="DejaVuBold", size=24, color=GOLD)
    # Feature boxes
    features = [
        ("QR Code", "Scannable BOLT11\ninvoice", CYAN),
        ("Copy Button", "One-click invoice\ncopy", GREEN),
        ("Payment Detection", "Auto-detect when\npaid (polling)", YELLOW),
        ("GitHub Pages", "Free hosting\nfrom your repo", ACCENT),
    ]
    box_w, box_h = 160, 70
    total_w = len(features) * box_w + (len(features) - 1) * 20
    start_x = (W - total_w) / 2
    y = H - 320
    for i, (label, desc, color) in enumerate(features):
        x = start_x + i * (box_w + 20)
        _box(c, x, y, box_w, box_h, border_color=color)
        _text(c, x + 12, y + box_h - 22, label, font="DejaVuBold", size=13, color=color)
        lines = desc.split("\n")
        for j, line in enumerate(lines):
            _text(c, x + 12, y + box_h - 40 - j * 14, line, font="Mono", size=9, color=DIM)
    # Reference
    _text_center(c, 90, "Live demo: https://pretyflaco.github.io/africafreerouting/",
                 font="Mono", size=12, color=CYAN)
    _text_center(c, 65, "Source: https://github.com/pretyflaco/africafreerouting",
                 font="Mono", size=12, color=DIM)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 3); c.showPage()


def slide_04_toolbox(c, blink_png):
    """The Toolbox — pipeline diagram."""
    _bg(c)
    _title(c, "The Toolbox")
    # Pipeline
    pipeline = [
        ("Terminal", CYAN, "Linux / WSL"),
        ("GitHub CLI", GREEN, "gh repo, gh pages"),
        ("OpenCode", ACCENT, "AI coding agent"),
        ("LLM", YELLOW, "MiniMax M2.5"),
        ("GitHub\nPages", GREEN, "Free hosting"),
    ]
    box_w, box_h = 120, 50
    total_w = len(pipeline) * box_w + (len(pipeline) - 1) * 25
    start_x = (W - total_w) / 2
    y_center = H - 210
    for i, (label, color, desc) in enumerate(pipeline):
        x = start_x + i * (box_w + 25)
        _box(c, x, y_center - box_h / 2, box_w, box_h, border_color=color)
        lines = label.split("\n")
        for j, line in enumerate(lines):
            lw = c.stringWidth(line, "DejaVuBold", 12)
            _text(c, x + (box_w - lw) / 2, y_center + 8 - j * 16, line,
                  font="DejaVuBold", size=12, color=color)
        dw = c.stringWidth(desc, "Mono", 9)
        _text(c, x + (box_w - dw) / 2, y_center - box_h / 2 - 16, desc,
              font="Mono", size=9, color=DIM)
        if i < len(pipeline) - 1:
            ax = x + box_w + 4
            c.setStrokeColorRGB(*DIM); c.setLineWidth(1)
            c.line(ax, y_center, ax + 17, y_center)
            _text(c, ax + 14, y_center - 5, "→", font="DejaVu", size=14, color=DIM)
    # Cost comparison
    y = H - 340
    _text(c, 80, y, "Cost Comparison:", font="DejaVuBold", size=16, color=CYAN)
    y -= 35
    costs = [
        ("MiniMax M2.5 via PPQ.ai", "~$0.30 / session", GREEN),
        ("Claude Opus", "~$25 / session", RED),
        ("PPQ.ai top-up", "Pay with Lightning — no subscription", YELLOW),
    ]
    for label, cost, color in costs:
        _text(c, 100, y, "▸", font="DejaVu", size=14, color=color)
        _text(c, 120, y, label, font="DejaVu", size=14, color=FG)
        _text(c, 420, y, cost, font="MonoBold", size=13, color=color)
        y -= 28
    # Chrome DevTools
    y -= 15
    _text(c, 80, y, "Bonus:", font="DejaVuBold", size=14, color=DIM)
    _text(c, 140, y, "Chrome DevTools MCP — the AI agent drives your browser",
          font="DejaVu", size=13, color=ACCENT)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 4); c.showPage()


def slide_05_why_lightning(c, blink_png):
    """Why Lightning for Africa?"""
    _bg(c)
    _title(c, "Why Lightning for Africa?")
    # Lightning bolt unicode
    _text_center(c, H - 140, "⚡", font="DejaVu", size=60, color=GOLD)
    y = H - 210
    reasons = [
        ("No bank account needed", "2/3 of Sub-Saharan Africa is unbanked"),
        ("Instant settlement", "No waiting days for payment clearance"),
        ("Micro-transactions viable", "Send 10 sats (~$0.001) — try that with Visa"),
        ("Cross-border without friction", "No currency conversion, no intermediaries"),
        ("Open infrastructure", "Anyone can build on it — no permission needed"),
        ("Growing African adoption", "Nigeria, Kenya, Ghana, South Africa leading the way"),
    ]
    for label, desc in reasons:
        _text(c, 120, y, "⚡", font="DejaVu", size=16, color=GOLD)
        _text(c, 150, y, label, font="DejaVuBold", size=16, color=FG)
        _text(c, 150, y - 20, desc, font="DejaVu", size=12, color=DIM)
        y -= 50
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 5); c.showPage()


def slide_06_blink_api(c, blink_png):
    """The Blink API (No Auth) — 2-step flow."""
    _bg(c)
    _title(c, "The Blink API (No Auth Required)")
    _text(c, 60, H - 115, "Two-step invoice creation — completely public, no API key",
          font="DejaVu", size=14, color=DIM)
    # Step 1 box
    s1_x, s1_y, s1_w, s1_h = 60, H - 270, 350, 100
    _box(c, s1_x, s1_y, s1_w, s1_h, border_color=CYAN)
    _text(c, s1_x + 15, s1_y + s1_h - 25, "Step 1: Get Wallet ID", font="DejaVuBold", size=14, color=CYAN)
    _text(c, s1_x + 15, s1_y + s1_h - 50, "accountDefaultWallet(", font="Mono", size=11, color=FG)
    _text(c, s1_x + 30, s1_y + s1_h - 68, 'username: "pretyflaco"', font="Mono", size=11, color=YELLOW)
    _text(c, s1_x + 30, s1_y + s1_h - 86, "walletCurrency: BTC )", font="Mono", size=11, color=FG)
    # Arrow
    _text(c, s1_x + s1_w + 15, s1_y + s1_h / 2 - 5, "→", font="DejaVuBold", size=24, color=GREEN)
    _text(c, s1_x + s1_w + 10, s1_y + s1_h / 2 - 25, "walletId", font="Mono", size=10, color=GREEN)
    # Step 2 box
    s2_x = s1_x + s1_w + 60
    s2_w = W - s2_x - 60
    _box(c, s2_x, s1_y, s2_w, s1_h, border_color=GREEN)
    _text(c, s2_x + 15, s1_y + s1_h - 25, "Step 2: Create Invoice", font="DejaVuBold", size=14, color=GREEN)
    _text(c, s2_x + 15, s1_y + s1_h - 50, "lnInvoiceCreateOnBehalfOf", font="Mono", size=10, color=FG)
    _text(c, s2_x + 15, s1_y + s1_h - 66, "  Recipient(", font="Mono", size=10, color=FG)
    _text(c, s2_x + 30, s1_y + s1_h - 82, "recipientWalletId, amount: 100)", font="Mono", size=9, color=YELLOW)
    # Result
    result_y = s1_y - 50
    _text_center(c, result_y, "→  BOLT11 Invoice  →  QR Code  →  Payment!",
                 font="DejaVuBold", size=18, color=GOLD)
    # References
    _text(c, 60, 90, "API Playbook:", font="DejaVuBold", size=12, color=DIM)
    _text(c, 180, 90, "dev.blink.sv/api/agent-playbook", font="Mono", size=12, color=CYAN)
    _text(c, 60, 65, "No-Auth Ops:", font="DejaVuBold", size=12, color=DIM)
    _text(c, 180, 65, "dev.blink.sv/api/no-api-key-operations", font="Mono", size=12, color=CYAN)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 6); c.showPage()


def slide_07_prompt_strategy(c, blink_png):
    """The Prompt Strategy — sequential prompts."""
    _bg(c)
    _title(c, "The Prompt Strategy")
    _text_center(c, H - 130, "Small prompts > mega prompts",
                 font="DejaVuBold", size=22, color=YELLOW)
    _text_center(c, H - 160, "Better for learning AND for the AI",
                 font="DejaVu", size=14, color=DIM)
    # Steps
    steps = [
        ("1", "Create GitHub repo + scaffold HTML", CYAN),
        ("2", "Integrate Blink API (no-auth invoice creation)", GREEN),
        ("3", "Add QR code display + copy button", YELLOW),
        ("4", "Add payment status polling (every 3s)", ACCENT),
        ("5", "Deploy to GitHub Pages + test live", GOLD),
    ]
    y = H - 230
    for num, desc, color in steps:
        # Number circle
        cx = 140
        c.setFillColorRGB(*color)
        c.circle(cx, y + 6, 14, fill=1)
        _text(c, cx - 5, y, num, font="DejaVuBold", size=14, color=BG)
        # Description
        _text(c, cx + 30, y, desc, font="DejaVu", size=16, color=FG)
        # Arrow down
        if num != "5":
            c.setStrokeColorRGB(*DIM); c.setLineWidth(1)
            c.line(cx, y - 10, cx, y - 28)
            _text(c, cx - 4, y - 32, "↓", font="DejaVu", size=10, color=DIM)
        y -= 50
    # Time estimate
    _text_center(c, 65, "~40 minutes from blank terminal to live payment page",
                 font="DejaVu", size=14, color=GREEN)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 7); c.showPage()


def slide_08_payment_flow(c, blink_png):
    """Payment flow diagram."""
    _bg(c)
    _title(c, "Payment Flow")
    # Flow boxes
    flow = [
        ("User Scans\nQR Code", CYAN),
        ("Pays via\nLightning Wallet", YELLOW),
        ("Blink\nNetwork", ACCENT),
        ("Poll Status\n(every 3s)", GREEN),
        ("PAID ✓", GOLD),
    ]
    box_w, box_h = 130, 55
    total_w = len(flow) * box_w + (len(flow) - 1) * 20
    start_x = (W - total_w) / 2
    y_center = H - 220
    for i, (label, color) in enumerate(flow):
        x = start_x + i * (box_w + 20)
        _box(c, x, y_center - box_h / 2, box_w, box_h, border_color=color)
        lines = label.split("\n")
        for j, line in enumerate(lines):
            lw = c.stringWidth(line, "DejaVuBold", 12)
            _text(c, x + (box_w - lw) / 2, y_center + 8 - j * 16, line,
                  font="DejaVuBold", size=12, color=color)
        if i < len(flow) - 1:
            ax = x + box_w + 2
            _text(c, ax + 2, y_center - 5, "→", font="DejaVu", size=16, color=DIM)
    # Polling detail
    y = H - 320
    _text(c, 80, y, "Payment status check (no auth required):", font="DejaVuBold", size=14, color=CYAN)
    y -= 30
    # Code block
    code_lines = [
        ("query {", FG),
        ("  lnInvoicePaymentStatusByPaymentRequest(", FG),
        ('    input: { paymentRequest: "lnbc..." }', YELLOW),
        ("  ) { status }  # PENDING → PAID → ✓", GREEN),
        ("}", FG),
    ]
    _box(c, 80, y - len(code_lines) * 18 - 10, 500, len(code_lines) * 18 + 20, border_color=DIM)
    for line_text, color in code_lines:
        _text(c, 95, y, line_text, font="Mono", size=11, color=color)
        y -= 18
    # Note
    _text(c, 80, 80, "Note:", font="DejaVuBold", size=12, color=ORANGE)
    _text(c, 130, 80, "WebSocket subscription exists but requires API key auth.",
          font="DejaVu", size=12, color=DIM)
    _text(c, 130, 62, "Polling is the no-auth alternative — simple and effective.",
          font="DejaVu", size=12, color=DIM)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 8); c.showPage()


def slide_09_what_can_go_wrong(c, blink_png):
    """What Can Go Wrong — agent failure modes."""
    _bg(c)
    _title(c, "What Can Go Wrong")
    _text(c, 60, H - 115, "AI agents are powerful but imperfect. Watch for these:",
          font="DejaVu", size=14, color=DIM)
    y = H - 175
    failures = [
        ("❌", "Uses authenticated endpoints when told to use public ones",
         "Correct: \"Use the no-auth endpoints from dev.blink.sv\"", RED),
        ("❌", "Does generic web search instead of reading provided docs",
         "Correct: \"Read dev.blink.sv/api/agent-playbook directly\"", RED),
        ("❌", "Executes actions in plan mode without permission",
         "Correct: Monitor what the agent does, not just what it says", RED),
        ("❌", "Hallucinates API names or parameters",
         "Correct: Always verify against the actual API reference", RED),
        ("❌", "Says \"it's done\" without actually testing",
         "Correct: \"Test it yourself with curl\" — close the loop", RED),
    ]
    for icon, problem, fix, color in failures:
        _text(c, 80, y, icon, font="DejaVu", size=16, color=color)
        _text(c, 110, y, problem, font="DejaVu", size=13, color=FG)
        _text(c, 110, y - 18, fix, font="Mono", size=10, color=GREEN)
        y -= 52
    # Quote
    _text_center(c, 55, "\"Failure is the best teacher — show it, don't hide it.\"",
                 font="DejaVu", size=15, color=YELLOW)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 9); c.showPage()


def slide_10_frontend_backend(c, blink_png):
    """Frontend vs. Backend comparison."""
    _bg(c)
    _title(c, "Frontend vs. Backend")
    # Two columns
    col_w = 340
    col_h = 280
    gap = 40
    left_x = (W - 2 * col_w - gap) / 2
    right_x = left_x + col_w + gap
    col_y = H - 130 - col_h
    # Left column: Frontend
    _box(c, left_x, col_y, col_w, col_h, border_color=GREEN)
    _text(c, left_x + 15, col_y + col_h - 25, "Frontend (GitHub Pages)",
          font="DejaVuBold", size=16, color=GREEN)
    left_items = [
        "Free hosting",
        "Static HTML/CSS/JS",
        "No secrets to protect",
        "Donation button + QR code",
        "Invoice generation (no auth)",
        "Payment status polling",
    ]
    y = col_y + col_h - 55
    for item in left_items:
        _text(c, left_x + 20, y, "✓", font="DejaVu", size=13, color=GREEN)
        _text(c, left_x + 40, y, item, font="DejaVu", size=12, color=FG)
        y -= 24
    _text(c, left_x + 20, y - 10, "Cost: $0", font="DejaVuBold", size=14, color=GREEN)
    # Right column: Backend
    _box(c, right_x, col_y, col_w, col_h, border_color=YELLOW)
    _text(c, right_x + 15, col_y + col_h - 25, "Backend (VPS / CF Workers)",
          font="DejaVuBold", size=16, color=YELLOW)
    right_items = [
        "API keys stay secret",
        "Check account balance",
        "Fundraising thermometer",
        "Webhooks + notifications",
        "Database / state storage",
        "Custom business logic",
    ]
    y = col_y + col_h - 55
    for item in right_items:
        _text(c, right_x + 20, y, "▸", font="DejaVu", size=13, color=YELLOW)
        _text(c, right_x + 40, y, item, font="DejaVu", size=12, color=FG)
        y -= 24
    _text(c, right_x + 20, y - 10, "Cost: ~5 EUR/month", font="DejaVuBold", size=14, color=YELLOW)
    # Bottom message
    _text_center(c, 60, "Start frontend. Add backend when you need it.",
                 font="DejaVuBold", size=20, color=GOLD)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 10); c.showPage()


def slide_11_poc_mvp(c, blink_png):
    """POC → MVP staircase."""
    _bg(c)
    _title(c, "From POC to MVP")
    # Staircase
    stairs = [
        ("Spike", '"Can we do it?"', "Quick experiment", DIM, 0),
        ("POC", '"It works!"', "Today's donation page", CYAN, 1),
        ("Prototype", '"Users can try it"', "Add real features", YELLOW, 2),
        ("MVP", '"Ship it!"', "Minimum viable product", GREEN, 3),
    ]
    stair_w, stair_h = 160, 50
    base_x, base_y = 100, 120
    for label, quote, desc, color, level in stairs:
        x = base_x + level * 50
        y = base_y + level * (stair_h + 15)
        _box(c, x, y, stair_w, stair_h, border_color=color)
        _text(c, x + 12, y + stair_h - 20, label, font="DejaVuBold", size=14, color=color)
        _text(c, x + 12, y + 8, quote, font="DejaVu", size=11, color=FG)
        _text(c, x + stair_w + 15, y + stair_h / 2 - 5, desc, font="Mono", size=11, color=DIM)
    # Arrow showing "YOU ARE HERE"
    poc_x = base_x + 1 * 50 + stair_w + 15
    poc_y = base_y + 1 * (stair_h + 15) + stair_h / 2
    _text(c, poc_x + 160, poc_y - 5, "← YOU ARE HERE", font="DejaVuBold", size=13, color=GOLD)
    # Bottom message
    _text_center(c, 70, "Today we built a POC. What's YOUR next step?",
                 font="DejaVuBold", size=20, color=GOLD)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 11); c.showPage()


def slide_12_building_blocks(c, blink_png):
    """Free building blocks grid."""
    _bg(c)
    _title(c, "Building Blocks")
    _text(c, 60, H - 115, "Free and near-free tools to build real products:",
          font="DejaVu", size=14, color=DIM)
    blocks = [
        ("ntfy.sh", "Push notifications", "Free, no signup, no API key", ORANGE),
        ("GitHub Pages", "Web hosting", "Free static site hosting", GREEN),
        ("Blink API", "Lightning payments", "No-auth invoice creation", CYAN),
        ("PPQ.ai + Lightning", "AI model access", "Pay-as-you-go, ~$0.30/session", YELLOW),
        ("Cloudflare Workers", "Serverless backend", "Free tier: 100K requests/day", ACCENT),
        ("OpenCode", "AI coding agent", "Open source, runs in terminal", GREEN),
    ]
    cols = 2
    box_w = 340
    box_h = 60
    gap_x, gap_y = 30, 15
    start_x = (W - cols * box_w - (cols - 1) * gap_x) / 2
    start_y = H - 170
    for i, (name, category, desc, color) in enumerate(blocks):
        col = i % cols
        row = i // cols
        x = start_x + col * (box_w + gap_x)
        y = start_y - row * (box_h + gap_y)
        _box(c, x, y, box_w, box_h, border_color=color)
        _text(c, x + 12, y + box_h - 22, name, font="DejaVuBold", size=14, color=color)
        _text(c, x + 12, y + box_h - 40, category, font="DejaVu", size=11, color=FG)
        _text(c, x + 12, y + 8, desc, font="Mono", size=9, color=DIM)
    # Big message
    _text_center(c, 65, "You can build a real product for < $5/month",
                 font="DejaVuBold", size=20, color=GOLD)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    _slide_num(c, 12); c.showPage()


def slide_13_resources(c, blink_png):
    """Resources + QR code + Questions."""
    _bg(c)
    _title(c, "Resources & Next Steps")
    # QR code
    qr_img = _generate_qr_image("https://github.com/pretyflaco/africafreerouting")
    qr_x, qr_y, qr_size = 60, H - 370, 180
    if qr_img:
        try:
            img_reader = ImageReader(qr_img)
            c.drawImage(img_reader, qr_x, qr_y, width=qr_size, height=qr_size)
        except Exception:
            _box(c, qr_x, qr_y, qr_size, qr_size, border_color=DIM)
            _text(c, qr_x + 20, qr_y + qr_size / 2, "[QR Code]", font="DejaVu", size=14, color=DIM)
    else:
        _box(c, qr_x, qr_y, qr_size, qr_size, border_color=DIM)
        _text(c, qr_x + 20, qr_y + qr_size / 2, "[QR Code]", font="DejaVu", size=14, color=DIM)
    _text(c, qr_x, qr_y - 20, "Scan to open the repo", font="DejaVu", size=11, color=DIM)
    # Resources list
    rx = 280
    ry = H - 140
    resources = [
        ("GitHub Repo", "github.com/pretyflaco/africafreerouting", CYAN),
        ("Blink API Playbook", "dev.blink.sv/api/agent-playbook", GREEN),
        ("No-Auth Operations", "dev.blink.sv/api/no-api-key-operations", GREEN),
        ("PPQ.ai", "ppq.ai — top up with Lightning", YELLOW),
        ("OpenCode", "opencode.ai — AI coding agent", ACCENT),
        ("ntfy.sh", "ntfy.sh — free push notifications", ORANGE),
        ("Blink Dashboard", "dashboard.blink.sv", CYAN),
        ("Setup Guide", "In repo: masterclass/202604/SETUP.md", DIM),
    ]
    for label, url, color in resources:
        _text(c, rx, ry, label, font="DejaVuBold", size=12, color=color)
        _text(c, rx + 180, ry, url, font="Mono", size=10, color=DIM)
        ry -= 24
    # Questions
    _text_center(c, 80, "Questions?", font="DejaVuBold", size=36, color=GREEN)
    # Logos
    _draw_logo_afr(c, 20, 10, 150, 50)
    _draw_logo_blink(c, blink_png, W - 140, 15, 120, 40)
    # Instructor handles
    _text_center(c, 30, "@pretyflaco  ·  @k9ert  ·  @openoms", font="Mono", size=11, color=DIM)
    _slide_num(c, 13); c.showPage()


# ─── Generate ────────────────────────────────────────────────────────────

def generate():
    # Convert Blink SVG to PNG
    blink_png = _convert_blink_svg()

    c = canvas.Canvas(OUTPUT, pagesize=landscape(A4))
    c.setTitle("Africa Free Routing — Lightning Payment Integration Masterclass")
    c.setAuthor("@pretyflaco, @k9ert, @openoms")

    slide_01_title(c, blink_png)
    slide_02_series(c, blink_png)
    slide_03_what_we_build(c, blink_png)
    slide_04_toolbox(c, blink_png)
    slide_05_why_lightning(c, blink_png)
    slide_06_blink_api(c, blink_png)
    slide_07_prompt_strategy(c, blink_png)
    slide_08_payment_flow(c, blink_png)
    slide_09_what_can_go_wrong(c, blink_png)
    slide_10_frontend_backend(c, blink_png)
    slide_11_poc_mvp(c, blink_png)
    slide_12_building_blocks(c, blink_png)
    slide_13_resources(c, blink_png)

    c.save()
    print(f"Generated: {OUTPUT}")

    # Cleanup temp file
    if blink_png and os.path.exists(blink_png):
        os.unlink(blink_png)


if __name__ == "__main__":
    generate()
