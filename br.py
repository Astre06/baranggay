import json
import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# -------- Barangay Picker --------
def get_random_city_barangay(path="/home/username/data/philippine_provinces_cities_municipalities_and_barangays_2019v2.json"):
    if not os.path.exists(path):
        return None, None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        city_list = []
        for region_name, region_data in data.items():
            for province_name, province_data in region_data.get("province_list", {}).items():
                for municipality_name, municipality_data in province_data.get("municipality_list", {}).items():
                    barangays = municipality_data.get("barangay_list", [])
                    if barangays:
                        city_list.append((region_name, province_name, municipality_name, barangays))

        if not city_list:
            return None, None

        region, province, city_name, barangays = random.choice(city_list)
        barangay_name = random.choice(barangays)
        return region, province, city_name, barangay_name

    except Exception as e:
        print("❌ Error reading JSON:", e)
        return None, None, None, None



# -------- Telegram Bot Handlers --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send /city to get a random city & barangay in the Philippines.")

async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    region, province, city, barangay = get_random_city_barangay()
    if city and barangay:
        await update.message.reply_text(
            f"🎯 Region: {region}\n📍 Province: {province}\n🏙️ City/Municipality: {city}\n🏘️ Barangay: {barangay}"
        )
    else:
        await update.message.reply_text("⚠️ Could not fetch city/barangay. Check your JSON file path.")

# -------- Main --------
def main():
    # Replace with your actual Telegram bot token
    TOKEN = "8167798874:AAHhr2F6-GP4GhE2gNVPtmsopI9hdE4Tvo4"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("city", city))

    print("✅ Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
