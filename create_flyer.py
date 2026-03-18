#!/usr/bin/env python3
"""薬局チラシ PDF生成スクリプト - 株式会社ジェームス「お薬やめれるかも」"""

from fpdf import FPDF
from PIL import Image
import os

# === 設定 ===
OUTPUT_PATH = "チラシ.pdf"
FONT_PATH_W3 = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"
FONT_PATH_W6 = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_PATH_W8 = "/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc"
FONT_PATH_MARU = "/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"

LOGO_PATH = "logo.png"
PHARMACY_IMG = "pharmacy2.jpg"
SHINOHARA_IMG = "/Users/nodakohei/Downloads/スクリーンショット_2023-07-31_20.21.55.png"

# A4 dimensions in mm
PAGE_W = 210
PAGE_H = 297
MARGIN = 12


class FlyerPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.add_font("gothic_w3", "", FONT_PATH_W3, uni=True)
        self.add_font("gothic_w6", "", FONT_PATH_W6, uni=True)
        self.add_font("gothic_w8", "", FONT_PATH_W8, uni=True)
        self.add_font("maru", "", FONT_PATH_MARU, uni=True)
        self.set_auto_page_break(auto=False)

    def rounded_rect(self, x, y, w, h, r, style="", fill_color=None, draw_color=None):
        """Draw a rounded rectangle."""
        if fill_color:
            self.set_fill_color(*fill_color)
        if draw_color:
            self.set_draw_color(*draw_color)

        # Use basic rect as fallback since fpdf2 rounded_rect needs specific handling
        if style == "F":
            self.rect(x, y, w, h, "F")
        elif style == "D":
            self.rect(x, y, w, h, "D")
        elif style == "DF":
            self.rect(x, y, w, h, "DF")


def prepare_shinohara_image():
    """篠原さんの画像をJPGに変換"""
    out_path = "shinohara.jpg"
    if not os.path.exists(out_path):
        img = Image.open(SHINOHARA_IMG)
        img = img.convert("RGB")
        # Crop to make it more portrait-like (center crop)
        w, h = img.size
        crop_w = int(h * 0.85)
        left = (w - crop_w) // 2
        img = img.crop((left, 0, left + crop_w, h))
        img.save(out_path, "JPEG", quality=95)
    return out_path


def create_flyer():
    pdf = FlyerPDF()
    pdf.add_page()

    # ============================================
    # 背景色: 薄いグリーン系（ヘルシーなイメージ）
    # ============================================
    pdf.set_fill_color(245, 250, 245)
    pdf.rect(0, 0, PAGE_W, PAGE_H, "F")

    # ============================================
    # トップバー（濃いグリーン）
    # ============================================
    pdf.set_fill_color(46, 125, 50)
    pdf.rect(0, 0, PAGE_W, 24, "F")

    # 社名
    pdf.set_font("gothic_w6", size=11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(MARGIN, 4)
    pdf.cell(0, 6, "株式会社ジェームス")

    pdf.set_font("gothic_w3", size=7)
    pdf.set_xy(MARGIN, 11)
    pdf.cell(0, 5, "東京・神奈川・千葉  調剤薬局グループ")

    # ロゴ（右上）
    try:
        logo_w = 40
        pdf.image(LOGO_PATH, x=PAGE_W - MARGIN - logo_w, y=2, w=logo_w)
    except Exception:
        pass

    y = 24

    # ============================================
    # メインキャッチコピー
    # ============================================
    pdf.set_fill_color(255, 248, 225)
    pdf.rect(0, y, PAGE_W, 45, "F")

    # 小さなリード
    pdf.set_font("maru", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(0, y + 3)
    pdf.cell(PAGE_W, 6, "毎日のお薬、本当に必要ですか？", align="C")

    # メインタイトル
    pdf.set_font("gothic_w8", size=34)
    pdf.set_text_color(46, 125, 50)
    pdf.set_xy(0, y + 11)
    pdf.cell(PAGE_W, 18, "お薬、やめれるかも。", align="C")

    # サブタイトル
    pdf.set_font("gothic_w6", size=12)
    pdf.set_text_color(80, 80, 80)
    pdf.set_xy(0, y + 32)
    pdf.cell(PAGE_W, 7, "ミネラルファスティングで、体の内側から変わる新習慣", align="C")

    y += 45

    # 区切り線
    pdf.set_draw_color(46, 125, 50)
    pdf.set_line_width(0.8)
    pdf.line(MARGIN + 30, y + 2, PAGE_W - MARGIN - 30, y + 2)
    y += 5

    # ============================================
    # 個別相談のご案内セクション
    # ============================================
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 50, "F")
    pdf.set_draw_color(200, 220, 200)
    pdf.set_line_width(0.3)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 50, "D")

    # セクションタイトル
    # ラベル背景
    label_w = 70
    label_x = (PAGE_W - label_w) / 2
    pdf.set_fill_color(46, 125, 50)
    pdf.rect(label_x, y - 4, label_w, 8, "F")
    pdf.set_font("gothic_w6", size=11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(label_x, y - 3.5)
    pdf.cell(label_w, 7, "無料 個別相談のご案内", align="C")

    pdf.set_font("gothic_w3", size=9.5)
    pdf.set_text_color(60, 60, 60)
    inner_margin = MARGIN + 8
    text_w = PAGE_W - 2 * inner_margin

    texts = [
        "「薬を減らしたい」「体質を根本から改善したい」",
        "そんなお悩みはありませんか？",
        "",
        "当薬局では、ミネラルファスティング（酵素断食）を",
        "取り入れた体質改善の個別相談を行っています。",
        "",
        "ファスティングとは、一定期間固形物を控え、",
        "必要なミネラル・ビタミンを摂りながら体をリセットする健康法。",
        "内臓を休め、代謝を高め、体本来の力を引き出します。",
    ]

    ty = y + 7
    for line in texts:
        if line == "":
            ty += 2
            continue
        pdf.set_xy(inner_margin, ty)
        pdf.cell(text_w, 5, line, align="C")
        ty += 5

    y += 50

    # ============================================
    # 篠原さん推薦セクション
    # ============================================
    pdf.set_fill_color(232, 245, 233)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 68, "F")
    pdf.set_draw_color(46, 125, 50)
    pdf.set_line_width(0.5)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 68, "D")

    # 篠原さんの写真
    shinohara_jpg = prepare_shinohara_image()
    img_w = 35
    img_h = 35
    img_x = MARGIN + 8
    img_y = y + 5

    try:
        pdf.image(shinohara_jpg, x=img_x, y=img_y, w=img_w, h=img_h)
    except Exception:
        pass

    # 名前ラベル
    pdf.set_font("gothic_w6", size=8)
    pdf.set_text_color(46, 125, 50)
    pdf.set_xy(img_x, img_y + img_h + 1)
    pdf.cell(img_w, 4, "代表 篠原", align="C")

    # 吹き出しテキスト
    bubble_x = img_x + img_w + 8
    bubble_w = PAGE_W - MARGIN - 8 - bubble_x

    pdf.set_font("gothic_w6", size=11)
    pdf.set_text_color(46, 125, 50)
    pdf.set_xy(bubble_x, y + 5)
    pdf.cell(bubble_w, 7, "代表 篠原のおすすめです！")

    pdf.set_font("gothic_w3", size=9)
    pdf.set_text_color(60, 60, 60)

    recommend_texts = [
        "私自身、ミネラルファスティングを体験し、",
        "体調の変化を実感しました。",
        "朝の目覚め、体の軽さ、集中力の向上――",
        "薬に頼らない健康づくりの第一歩として、",
        "ぜひ多くの方に知っていただきたいと思い、",
        "当薬局での個別相談をスタートしました。",
    ]

    ry = y + 14
    for line in recommend_texts:
        pdf.set_xy(bubble_x, ry)
        pdf.cell(bubble_w, 4.8, line)
        ry += 4.8

    # 薬局写真（小さく右下に）
    try:
        ph_w = 30
        ph_h = 20
        pdf.image(PHARMACY_IMG, x=PAGE_W - MARGIN - ph_w - 5, y=y + 40, w=ph_w, h=ph_h)
    except Exception:
        pass

    y += 65

    # ============================================
    # 指導者紹介セクション
    # ============================================
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 26, "F")
    pdf.set_draw_color(200, 220, 200)
    pdf.set_line_width(0.3)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 26, "D")

    # ラベル
    label_w2 = 50
    label_x2 = (PAGE_W - label_w2) / 2
    pdf.set_fill_color(255, 152, 0)
    pdf.rect(label_x2, y - 4, label_w2, 8, "F")
    pdf.set_font("gothic_w6", size=10)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(label_x2, y - 3.5)
    pdf.cell(label_w2, 7, "あなたの相談相手", align="C")

    pdf.set_font("gothic_w8", size=14)
    pdf.set_text_color(60, 60, 60)
    pdf.set_xy(0, y + 5)
    pdf.cell(PAGE_W, 8, "ファスティング指導担当  浩代", align="C")

    pdf.set_font("gothic_w3", size=8.5)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(0, y + 15)
    pdf.cell(PAGE_W, 5, "お一人おひとりの体調やお悩みに合わせて、丁寧にサポートいたします。", align="C")

    y += 30

    # ============================================
    # こんな方におすすめ
    # ============================================
    pdf.set_fill_color(255, 243, 224)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 34, "F")
    pdf.set_draw_color(255, 152, 0)
    pdf.set_line_width(0.3)
    pdf.rect(MARGIN, y, PAGE_W - 2 * MARGIN, 34, "D")

    pdf.set_font("gothic_w6", size=10)
    pdf.set_text_color(230, 120, 0)
    pdf.set_xy(MARGIN + 5, y + 2)
    pdf.cell(0, 6, "こんな方におすすめ")

    items = [
        "お薬の量を減らしたい方",
        "生活習慣病の予防・改善をしたい方",
        "体質を根本から見直したい方",
        "ダイエットや美容にも興味がある方",
    ]

    iy = y + 9
    for item in items:
        # Green circle bullet
        pdf.set_fill_color(46, 125, 50)
        cx = MARGIN + 10
        cy = iy + 2.5
        pdf.ellipse(cx - 1.5, cy - 1.5, 3, 3, "F")
        # Item text
        pdf.set_font("maru", size=9.5)
        pdf.set_text_color(80, 80, 80)
        pdf.set_xy(MARGIN + 15, iy)
        pdf.cell(0, 5.5, item)
        iy += 6

    y += 37

    # ============================================
    # フッター: 相談予約・連絡先
    # ============================================
    footer_h = PAGE_H - y
    pdf.set_fill_color(46, 125, 50)
    pdf.rect(0, y, PAGE_W, footer_h, "F")

    pdf.set_font("gothic_w8", size=13)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, y + 3)
    pdf.cell(PAGE_W, 7, "まずはお気軽にご相談ください", align="C")

    pdf.set_font("gothic_w6", size=9)
    pdf.set_xy(0, y + 11)
    pdf.cell(PAGE_W, 5, "ご予約・お問い合わせ", align="C")

    # プレースホルダー（後で追加する連絡先）
    pdf.set_fill_color(255, 255, 255)
    box_w = 140
    box_x = (PAGE_W - box_w) / 2
    box_y = y + 18
    pdf.rect(box_x, box_y, box_w, 14, "F")

    pdf.set_font("gothic_w6", size=11)
    pdf.set_text_color(46, 125, 50)
    pdf.set_xy(box_x, box_y + 1)
    pdf.cell(box_w, 6, "TEL: ___-____-____", align="C")

    pdf.set_font("gothic_w3", size=7.5)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(box_x, box_y + 7.5)
    pdf.cell(box_w, 5, "受付時間: ____〜____  /  店舗名: __________", align="C")

    # 最下部: 会社情報
    pdf.set_font("gothic_w3", size=6.5)
    pdf.set_text_color(200, 230, 200)
    pdf.set_xy(0, PAGE_H - 5)
    pdf.cell(PAGE_W, 4, "株式会社ジェームス  |  東京・神奈川・千葉  調剤薬局グループ", align="C")

    # === 出力 ===
    pdf.output(OUTPUT_PATH)
    print(f"チラシを生成しました: {os.path.abspath(OUTPUT_PATH)}")


if __name__ == "__main__":
    create_flyer()
