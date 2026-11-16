"""
User-facing translations for the bot.

Every language is written in its own native script only.
Missing keys fall back to English, then to the key name itself.
"""

# (language_code, native_name) - native_name is shown in the language picker
LANGUAGES = [
    ("en", "English"),
    ("hi", "हिन्दी"),
    ("mr", "मराठी"),
    ("bn", "বাংলা"),
    ("ta", "தமிழ்"),
    ("te", "తెలుగు"),
    ("kn", "ಕನ್ನಡ"),
    ("ml", "മലയാളം"),
    ("ur", "اردو"),
    ("pa", "ਪੰਜਾਬੀ"),
    ("gu", "ગુજરાતી"),
    ("es", "Español"),
    ("fr", "Français"),
    ("de", "Deutsch"),
]

LANGUAGE_CODES = {code for code, _name in LANGUAGES}

TRANSLATIONS = {}

TRANSLATIONS["en"] = {
    "welcome": "🌟 {mention}, I am a Terabox downloader bot. Send me any Terabox link, I will download it within a few seconds and send it to you ✨.",
    "must_join": "You must join my channel to use me.",
    "cooldown": "The API is under development. To reduce abuse you must wait {remaining}s.",
    "invalid_link": "Please provide a valid Terabox link.",
    "sending_media": "Sending you the media...🤤",
    "download_failed": (
        "Download failed ❌\n\n"
        "Reason: the link may be broken or it's a folder link.\n"
        "Only file links are supported."
    ),
    "file_deleted_warning": "⚠️ This file will be auto-deleted in 10 minutes. Forward it to save.",
    "no_videos": "No videos indexed yet. Owner can use /refresh to build the index.",
    "mongo_missing": "MongoDB is not configured.",
    "search_usage": "Usage: /search <1 to 3 keywords>",
    "search_no_results": "No files found matching all supplied keywords.",
    "search_unavailable": "Search is temporarily unavailable. Please try again.",
    "search_expired": "This search has expired. Send /search again.",
    "search_not_yours": "This search belongs to another user.",
    "search_none_left": "No matching files are available anymore.",
    "search_send_failed": "Failed to send this file. It may have been removed from the source channel.",
    "search_header": "🔎 Search: {keywords}\nFound {count} matching files. Select a filename below.",
    "search_sending": "Sending file...",
    "search_file_unavailable": "This file is no longer available.",
    "dump_caption": (
        "💾 Permanent Dump Channel Access\n\n"
        "Buy permanent access to the whole dump channel.\n\n"
        "• Binance: 1.5 USDT only\n"
        "• UPI: ₹200 only\n\n"
        "Choose your payment method below. After paying, send the payment "
        "screenshot to @rtx5069 for verification."
    ),
    "dump_qr_binance": (
        "Binance Payment\n\n"
        "Amount: 1.5 USDT only\n\n"
        "Scan this QR using the Binance app. After paying, send the "
        "payment screenshot to @rtx5069 for verification."
    ),
    "dump_qr_upi": (
        "UPI Payment\n\n"
        "Amount: ₹200 only\n\n"
        "Scan this QR using any UPI app. After paying, send the payment "
        "screenshot to @rtx5069 for verification."
    ),
    "dump_qr_error": "Could not display the payment QR. Please send /dump and try again.",
    "dump_unavailable": "Dump access information is temporarily unavailable.",
    "dump_menu_unavailable": "Payment menu is temporarily unavailable.",
    "select_language": "🌐 Select your language:",
    "language_saved": "✅ Language set: {language}",
    "confirm": "✅ Confirm",
    "settings_title": "⚙️ User Settings",
}

TRANSLATIONS["hi"] = {
    "welcome": "🌟 {mention}, मैं एक टेराबॉक्स डाउनलोडर बॉट हूँ। मुझे कोई भी टेराबॉक्स लिंक भेजें, मैं इसे कुछ सेकंड में डाउनलोड करके आपको भेज दूँगा ✨।",
    "must_join": "मेरा उपयोग करने के लिए आपको मेरे चैनल से जुड़ना होगा।",
    "cooldown": "एपीआई विकास के अंतर्गत है। दुरुपयोग कम करने के लिए आपको {remaining} सेकंड प्रतीक्षा करनी होगी।",
    "invalid_link": "कृपया एक मान्य टेराबॉक्स लिंक प्रदान करें।",
    "sending_media": "आपको मीडिया भेज रहा हूँ...🤤",
    "download_failed": (
        "डाउनलोड विफल ❌\n\n"
        "कारण: लिंक टूटा हुआ हो सकता है या यह फ़ोल्डर लिंक है।\n"
        "केवल फ़ाइल लिंक समर्थित हैं।"
    ),
    "file_deleted_warning": "⚠️ यह फ़ाइल 10 मिनट में स्वतः हटा दी जाएगी। सहेजने के लिए फ़ॉरवर्ड करें।",
    "no_videos": "अभी कोई वीडियो इंडेक्स नहीं हुआ है। इंडेक्स बनाने के लिए मालिक /refresh का उपयोग कर सकता है।",
    "mongo_missing": "MongoDB कॉन्फ़िगर नहीं है।",
    "search_usage": "उपयोग: /search <1 से 3 कीवर्ड>",
    "search_no_results": "दी गई सभी कीवर्ड से मेल खाती कोई फ़ाइल नहीं मिली।",
    "search_unavailable": "खोज अस्थायी रूप से उपलब्ध नहीं है। कृपया पुनः प्रयास करें।",
    "search_expired": "यह खोज समाप्त हो गई है। /search फिर से भेजें।",
    "search_not_yours": "यह खोज किसी अन्य उपयोगकर्ता की है।",
    "search_none_left": "अब कोई मेल खाती फ़ाइल उपलब्ध नहीं है।",
    "search_send_failed": "यह फ़ाइल भेजने में विफल। संभवतः इसे स्रोत चैनल से हटा दिया गया है।",
    "search_header": "🔎 खोज: {keywords}\n{count} मेल खाती फ़ाइलें मिलीं। नीचे से फ़ाइल नाम चुनें।",
    "search_sending": "फ़ाइल भेज रहा हूँ...",
    "search_file_unavailable": "यह फ़ाइल अब उपलब्ध नहीं है।",
    "dump_caption": (
        "💾 स्थायी डंप चैनल एक्सेस\n\n"
        "पूरे डंप चैनल की स्थायी एक्सेस खरीदें।\n\n"
        "• Binance: केवल 1.5 USDT\n"
        "• UPI: केवल ₹200\n\n"
        "नीचे अपनी भुगतान विधि चुनें। भुगतान के बाद, सत्यापन के लिए भुगतान "
        "स्क्रीनशॉट @rtx5069 को भेजें।"
    ),
    "dump_qr_binance": (
        "Binance भुगतान\n\n"
        "राशि: केवल 1.5 USDT\n\n"
        "Binance ऐप से यह QR स्कैन करें। भुगतान के बाद, सत्यापन के लिए भुगतान "
        "स्क्रीनशॉट @rtx5069 को भेजें।"
    ),
    "dump_qr_upi": (
        "UPI भुगतान\n\n"
        "राशि: केवल ₹200\n\n"
        "किसी भी UPI ऐप से यह QR स्कैन करें। भुगतान के बाद, सत्यापन के लिए भुगतान "
        "स्क्रीनशॉट @rtx5069 को भेजें।"
    ),
    "dump_qr_error": "भुगतान QR नहीं दिखाया जा सका। कृपया /dump भेजकर पुनः प्रयास करें।",
    "dump_unavailable": "डंप एक्सेस जानकारी अस्थायी रूप से उपलब्ध नहीं है।",
    "dump_menu_unavailable": "भुगतान मेन्यू अस्थायी रूप से उपलब्ध नहीं है।",
    "select_language": "🌐 अपनी भाषा चुनें:",
    "language_saved": "✅ चयनित भाषा: {language}",
    "confirm": "✅ पुष्टि करें",
    "settings_title": "⚙️ उपयोगकर्ता सेटिंग्स",
}

TRANSLATIONS["mr"] = {
    "welcome": "🌟 {mention}, मी एक टेराबॉक्स डाउनलोडर बॉट आहे. मला कोणताही टेराबॉक्स लिंक पाठवा, मी तो काही सेकंदांत डाउनलोड करून तुम्हाला पाठवेन ✨.",
    "must_join": "माझा वापर करण्यासाठी तुम्ही माझ्या चॅनेलशी जोडलेले असले पाहिजे.",
    "cooldown": "एपीआय विकासाधीन आहे. गैरवापर कमी करण्यासाठी तुम्ही {remaining} सेकंद थांबले पाहिजे.",
    "invalid_link": "कृपया वैध टेराबॉक्स लिंक द्या.",
    "sending_media": "तुम्हाला मीडिया पाठवत आहे...🤤",
    "download_failed": (
        "डाउनलोड अयशस्वी ❌\n\n"
        "कारण: लिंक खराब असू शकतो किंवा तो फोल्डर लिंक आहे.\n"
        "फक्त फाइल लिंक सपोर्टेड आहेत."
    ),
    "file_deleted_warning": "⚠️ ही फाइल 10 मिनिटांत आपोआप हटविली जाईल. जतन करण्यासाठी फॉरवर्ड करा.",
    "no_videos": "अजून कोणतेही व्हिडिओ इंडेक्स केलेले नाहीत. अनुक्रमणिका बनवण्यासाठी मालक /refresh वापरू शकतो.",
    "mongo_missing": "MongoDB कॉन्फिगर केलेले नाही.",
    "search_usage": "वापर: /search <1 ते 3 कीवर्ड>",
    "search_no_results": "दिलेल्या सर्व कीवर्डशी जुळणारी कोणतीही फाइल सापडली नाही.",
    "search_unavailable": "शोध तात्पुरते अनुपलब्ध आहे. कृपया पुन्हा प्रयत्न करा.",
    "search_expired": "हा शोध कालबाह्य झाला आहे. /search पुन्हा पाठवा.",
    "search_not_yours": "हा शोध दुसऱ्या वापरकर्त्याचा आहे.",
    "search_none_left": "आता कोणतीही जुळणारी फाइल उपलब्ध नाही.",
    "search_send_failed": "ही फाइल पाठवण्यात अयशस्वी. कदाचित ती स्रोत चॅनेलमधून काढली गेली आहे.",
    "search_header": "🔎 शोध: {keywords}\n{count} जुळणाऱ्या फाइली सापडल्या. खाली फाइलचे नाव निवडा.",
    "search_sending": "फाइल पाठवत आहे...",
    "search_file_unavailable": "ही फाइल आता उपलब्ध नाही.",
    "dump_caption": (
        "💾 कायमस्वरूपी डंप चॅनल प्रवेश\n\n"
        "संपूर्ण डंप चॅनलचा कायमस्वरूपी प्रवेश खरेदी करा.\n\n"
        "• Binance: फक्त 1.5 USDT\n"
        "• UPI: फक्त ₹200\n\n"
        "खाली तुमची पेमेंट पद्धत निवडा. पेमेंटनंतर, पडताळणीसाठी पेमेंट "
        "स्क्रीनशॉट @rtx5069 यांना पाठवा."
    ),
    "dump_qr_binance": (
        "Binance पेमेंट\n\n"
        "रक्कम: फक्त 1.5 USDT\n\n"
        "Binance अॅपने हा QR स्कॅन करा. पेमेंटनंतर, पडताळणीसाठी पेमेंट "
        "स्क्रीनशॉट @rtx5069 यांना पाठवा."
    ),
    "dump_qr_upi": (
        "UPI पेमेंट\n\n"
        "रक्कम: फक्त ₹200\n\n"
        "कोणत्याही UPI अॅपने हा QR स्कॅन करा. पेमेंटनंतर, पडताळणीसाठी पेमेंट "
        "स्क्रीनशॉट @rtx5069 यांना पाठवा."
    ),
    "dump_qr_error": "पेमेंट QR दाखवता आला नाही. कृपया /dump पाठवून पुन्हा प्रयत्न करा.",
    "dump_unavailable": "डंप प्रवेश माहिती तात्पुरते अनुपलब्ध आहे.",
    "dump_menu_unavailable": "पेमेंट मेनू तात्पुरते अनुपलब्ध आहे.",
    "select_language": "🌐 तुमची भाषा निवडा:",
    "language_saved": "✅ निवडलेली भाषा: {language}",
    "confirm": "✅ पुष्टी करा",
    "settings_title": "⚙️ वापरकर्ता सेटिंग्ज",
}

TRANSLATIONS["bn"] = {
    "welcome": "🌟 {mention}, আমি একটি টেরাবক্স ডাউনলোডার বট। আমাকে যেকোনো টেরাবক্স লিংক পাঠান, আমি কয়েক সেকেন্ডে ডাউনলোড করে আপনাকে পাঠিয়ে দেব ✨।",
    "must_join": "আমাকে ব্যবহার করতে হলে আপনাকে আমার চ্যানেলে যোগ দিতে হবে।",
    "cooldown": "এপিআই উন্নয়নের অধীনে আছে। অপব্যবহার কমাতে আপনাকে {remaining} সেকেন্ড অপেক্ষা করতে হবে।",
    "invalid_link": "অনুগ্রহ করে একটি বৈধ টেরাবক্স লিংক দিন।",
    "sending_media": "আপনাকে মিডিয়া পাঠাচ্ছি...🤤",
    "download_failed": (
        "ডাউনলোড ব্যর্থ ❌\n\n"
        "কারণ: লিংকটি ভাঙা হতে পারে অথবা এটি একটি ফোল্ডার লিংক।\n"
        "শুধুমাত্র ফাইল লিংক সমর্থিত।"
    ),
    "file_deleted_warning": "⚠️ এই ফাইলটি 10 মিনিটে স্বয়ংক্রিয়ভাবে মুছে যাবে। সংরক্ষণ করতে ফরওয়ার্ড করুন।",
    "no_videos": "এখনও কোনো ভিডিও ইনডেক্স করা হয়নি। সূচি তৈরি করতে মালিক /refresh ব্যবহার করতে পারেন।",
    "mongo_missing": "MongoDB কনফিগার করা নেই।",
    "search_usage": "ব্যবহার: /search <১ থেকে ৩টি কীওয়ার্ড>",
    "search_no_results": "দেওয়া সব কীওয়ার্ডের সাথে মেলে এমন কোনো ফাইল পাওয়া যায়নি।",
    "search_unavailable": "সার্চ সাময়িকভাবে অনুপলব্ধ। অনুগ্রহ করে আবার চেষ্টা করুন।",
    "search_expired": "এই সার্চের মেয়াদ শেষ। /search আবার পাঠান।",
    "search_not_yours": "এই সার্চ অন্য ব্যবহারকারীর।",
    "search_none_left": "এখন আর কোনো মেলা ফাইল উপলব্ধ নেই।",
    "search_send_failed": "এই ফাইল পাঠানো ব্যর্থ হয়েছে। সম্ভবত এটি সোর্স চ্যানেল থেকে সরিয়ে ফেলা হয়েছে।",
    "search_header": "🔎 সার্চ: {keywords}\n{count}টি মেলা ফাইল পাওয়া গেছে। নিচ থেকে ফাইলের নাম নির্বাচন করুন।",
    "search_sending": "ফাইল পাঠাচ্ছি...",
    "search_file_unavailable": "এই ফাইলটি আর উপলব্ধ নেই।",
    "dump_caption": (
        "💾 স্থায়ী ডাম্প চ্যানেল অ্যাক্সেস\n\n"
        "সম্পূর্ণ ডাম্প চ্যানেলের স্থায়ী অ্যাক্সেস কিনুন।\n\n"
        "• Binance: মাত্র 1.5 USDT\n"
        "• UPI: মাত্র ₹200\n\n"
        "নিচে আপনার পেমেন্ট পদ্ধতি নির্বাচন করুন। পেমেন্টের পরে, যাচাইয়ের "
        "জন্য পেমেন্ট স্ক্রিনশট @rtx5069 কে পাঠান।"
    ),
    "dump_qr_binance": (
        "Binance পেমেন্ট\n\n"
        "পরিমাণ: মাত্র 1.5 USDT\n\n"
        "Binance অ্যাপ দিয়ে এই QR স্ক্যান করুন। পেমেন্টের পরে, যাচাইয়ের "
        "জন্য পেমেন্ট স্ক্রিনশট @rtx5069 কে পাঠান।"
    ),
    "dump_qr_upi": (
        "UPI পেমেন্ট\n\n"
        "পরিমাণ: মাত্র ₹200\n\n"
        "যেকোনো UPI অ্যাপ দিয়ে এই QR স্ক্যান করুন। পেমেন্টের পরে, যাচাইয়ের "
        "জন্য পেমেন্ট স্ক্রিনশট @rtx5069 কে পাঠান।"
    ),
    "dump_qr_error": "পেমেন্ট QR দেখানো যায়নি। অনুগ্রহ করে /dump পাঠিয়ে আবার চেষ্টা করুন।",
    "dump_unavailable": "ডাম্প অ্যাক্সেসের তথ্য সাময়িকভাবে অনুপলব্ধ।",
    "dump_menu_unavailable": "পেমেন্ট মেনু সাময়িকভাবে অনুপলব্ধ।",
    "select_language": "🌐 আপনার ভাষা নির্বাচন করুন:",
    "language_saved": "✅ নির্বাচিত ভাষা: {language}",
    "confirm": "✅ নিশ্চিত করুন",
    "settings_title": "⚙️ ব্যবহারকারীর সেটিংস",
}

TRANSLATIONS["ta"] = {
    "welcome": "🌟 {mention}, நான் ஒரு டெராபாக்ஸ் பதிவிறக்க பாட். எந்த டெராபாக்ஸ் இணைப்பையும் எனக்கு அனுப்புங்கள், சில விநாடிகளில் பதிவிறக்கி உங்களுக்கு அனுப்புவேன் ✨.",
    "must_join": "என்னைப் பயன்படுத்த நீங்கள் எனது சேனலில் சேர வேண்டும்.",
    "cooldown": "ஏபிஐ உருவாக்கத்தில் உள்ளது. துஷ்பிரயோகத்தைக் குறைக்க நீங்கள் {remaining} விநாடிகள் காத்திருக்க வேண்டும்.",
    "invalid_link": "தயவுசெய்து சரியான டெராபாக்ஸ் இணைப்பை வழங்கவும்.",
    "sending_media": "உங்களுக்கு மீடியா அனுப்புகிறேன்...🤤",
    "download_failed": (
        "பதிவிறக்கம் தோல்வி ❌\n\n"
        "காரணம்: இணைப்பு உடைந்திருக்கலாம் அல்லது அது கோப்புறை இணைப்பு.\n"
        "கோப்பு இணைப்புகள் மட்டுமே ஆதரிக்கப்படுகின்றன."
    ),
    "file_deleted_warning": "⚠️ இந்த கோப்பு 10 நிமிடங்களில் தானாக நீக்கப்படும். சேமிக்க ஃபார்வர்ட் செய்யுங்கள்.",
    "no_videos": "இன்னும் எந்த வீடியோவும் அட்டவணைப்படுத்தப்படவில்லை. அட்டவணையை உருவாக்க உரிமையாளர் /refresh பயன்படுத்தலாம்.",
    "mongo_missing": "MongoDB கட்டமைக்கப்படவில்லை.",
    "search_usage": "பயன்பாடு: /search <1 முதல் 3 சொற்கள்>",
    "search_no_results": "கொடுக்கப்பட்ட அனைத்து சொற்களுடனும் பொருந்தும் கோப்பு எதுவும் கிடைக்கவில்லை.",
    "search_unavailable": "தேடல் தற்காலிகமாக கிடைக்கவில்லை. மீண்டும் முயற்சிக்கவும்.",
    "search_expired": "இந்த தேடல் காலாவதியானது. /search மீண்டும் அனுப்பவும்.",
    "search_not_yours": "இந்த தேடல் மற்றொரு பயனருடையது.",
    "search_none_left": "இனி பொருந்தும் கோப்புகள் இல்லை.",
    "search_send_failed": "இந்த கோப்பை அனுப்ப முடியவில்லை. அது மூல சேனலிலிருந்து அகற்றப்பட்டிருக்கலாம்.",
    "search_header": "🔎 தேடல்: {keywords}\n{count} பொருந்தும் கோப்புகள் கிடைத்தன. கீழே கோப்பின் பெயரைத் தேர்ந்தெடுக்கவும்.",
    "search_sending": "கோப்பை அனுப்புகிறேன்...",
    "search_file_unavailable": "இந்த கோப்பு இப்போது கிடைக்கவில்லை.",
    "dump_caption": (
        "💾 நிரந்தர டம்ப் சேனல் அணுகல்\n\n"
        "முழு டம்ப் சேனலின் நிரந்தர அணுகலை வாங்குங்கள்.\n\n"
        "• Binance: 1.5 USDT மட்டும்\n"
        "• UPI: ₹200 மட்டும்\n\n"
        "கீழே உங்கள் பணம் செலுத்தும் முறையைத் தேர்ந்தெடுங்கள். பணம் "
        "செலுத்திய பிறகு, சரிபார்ப்புக்கு திரைப்படத்தை @rtx5069 க்கு அனுப்பவும்."
    ),
    "dump_qr_binance": (
        "Binance பணப்பரிமாற்றம்\n\n"
        "தொகை: 1.5 USDT மட்டும்\n\n"
        "Binance ஆப்பின் மூலம் இந்த QR ஐ ஸ்கேன் செய்யுங்கள். பணம் "
        "செலுத்திய பிறகு, சரிபார்ப்புக்கு ஸ்கிரீன்ஷாட்டை @rtx5069 க்கு அனுப்பவும்."
    ),
    "dump_qr_upi": (
        "UPI பணப்பரிமாற்றம்\n\n"
        "தொகை: ₹200 மட்டும்\n\n"
        "எந்த UPI ஆப்பின் மூலமும் இந்த QR ஐ ஸ்கேன் செய்யுங்கள். பணம் "
        "செலுத்திய பிறகு, சரிபார்ப்புக்கு ஸ்கிரீன்ஷாட்டை @rtx5069 க்கு அனுப்பவும்."
    ),
    "dump_qr_error": "பணம் செலுத்தும் QR-ஐக் காட்ட முடியவில்லை. /dump அனுப்பி மீண்டும் முயற்சிக்கவும்.",
    "dump_unavailable": "டம்ப் அணுகல் தகவல் தற்காலிகமாக கிடைக்கவில்லை.",
    "dump_menu_unavailable": "பணம் செலுத்தும் பட்டியல் தற்காலிகமாக கிடைக்கவில்லை.",
    "select_language": "🌐 உங்கள் மொழியைத் தேர்ந்தெடுங்கள்:",
    "language_saved": "✅ தேர்ந்தெடுத்த மொழி: {language}",
    "confirm": "✅ உறுதிசெய்",
    "settings_title": "⚙️ பயனர் அமைப்புகள்",
}

TRANSLATIONS["te"] = {
    "welcome": "🌟 {mention}, నేను ఒక టెరాబాక్స్ డౌన్‌లోడర్ బాట్. ఏదైనా టెరాబాక్స్ లింక్ పంపండి, కొన్ని సెకన్లలో డౌన్‌లోడ్ చేసి మీకు పంపుతాను ✨.",
    "must_join": "నన్ను ఉపయోగించడానికి మీరు నా ఛానల్‌లో చేరాలి.",
    "cooldown": "ఏపీఐ అభివృద్ధిలో ఉంది. దుర్వినియోగాన్ని తగ్గించడానికి మీరు {remaining} సెకన్లు వేచి ఉండాలి.",
    "invalid_link": "దయచేసి సరైన టెరాబాక్స్ లింక్ ఇవ్వండి.",
    "sending_media": "మీకు మీడియా పంపుతున్నాను...🤤",
    "download_failed": (
        "డౌన్‌లోడ్ విఫలమైంది ❌\n\n"
        "కారణం: లింక్ పనిచేయకపోవచ్చు లేదా అది ఫోల్డర్ లింక్.\n"
        "ఫైల్ లింక్‌లు మాత్రమే మద్దతు ఇస్తున్నాయి."
    ),
    "file_deleted_warning": "⚠️ ఈ ఫైల్ 10 నిమిషాల్లో స్వయంచాలకంగా తొలగించబడుతుంది. సేవ్ చేయడానికి ఫార్వర్డ్ చేయండి.",
    "no_videos": "ఇంకా ఏ వీడియోలు ఇండెక్స్ చేయబడలేదు. సూచికను నిర్మించడానికి యజమాని /refresh ఉపయోగించవచ్చు.",
    "mongo_missing": "MongoDB కాన్ఫిగర్ చేయబడలేదు.",
    "search_usage": "వాడుక: /search <1 నుండి 3 కీవర్డ్‌లు>",
    "search_no_results": "ఇచ్చిన అన్ని కీవర్డ్‌లకు సరిపోయే ఫైల్ ఏదీ కనుగొనబడలేదు.",
    "search_unavailable": "శోధన తాత్కాలికంగా అందుబాటులో లేదు. దయచేసి మళ్లీ ప్రయత్నించండి.",
    "search_expired": "ఈ శోధన గడువు ముగిసింది. /search మళ్లీ పంపండి.",
    "search_not_yours": "ఈ శోధన మరొక వినియోగదారుది.",
    "search_none_left": "ఇప్పుడు సరిపోయే ఫైళ్లు లేవు.",
    "search_send_failed": "ఈ ఫైల్‌ను పంపడంలో విఫలమైంది. బహుశా అది మూల ఛానల్ నుండి తీసివేయబడి ఉండవచ్చు.",
    "search_header": "🔎 శోధన: {keywords}\n{count} సరిపోయే ఫైళ్లు దొరికాయి. దిగువ ఫైల్ పేరును ఎంచుకోండి.",
    "search_sending": "ఫైల్ పంపుతున్నాను...",
    "search_file_unavailable": "ఈ ఫైల్ ఇప్పుడు అందుబాటులో లేదు.",
    "dump_caption": (
        "💾 శాశ్వత డంప్ ఛానల్ యాక్సెస్\n\n"
        "మొత్తం డంప్ ఛానల్‌కు శాశ్వత యాక్సెస్ కొనండి.\n\n"
        "• Binance: 1.5 USDT మాత్రమే\n"
        "• UPI: ₹200 మాత్రమే\n\n"
        "దిగువ మీ చెల్లింపు విధానాన్ని ఎంచుకోండి. చెల్లింపు తర్వాత, "
        "ధృవీకరణ కోసం స్క్రీన్‌షాట్‌ను @rtx5069 కు పంపండి."
    ),
    "dump_qr_binance": (
        "Binance చెల్లింపు\n\n"
        "మొత్తం: 1.5 USDT మాత్రమే\n\n"
        "Binance యాప్‌తో ఈ QR ను స్కాన్ చేయండి. చెల్లింపు తర్వాత, "
        "ధృవీకరణ కోసం స్క్రీన్‌షాట్‌ను @rtx5069 కు పంపండి."
    ),
    "dump_qr_upi": (
        "UPI చెల్లింపు\n\n"
        "మొత్తం: ₹200 మాత్రమే\n\n"
        "ఏ UPI యాప్‌తోనైనా ఈ QR ను స్కాన్ చేయండి. చెల్లింపు తర్వాత, "
        "ధృవీకరణ కోసం స్క్రీన్‌షాట్‌ను @rtx5069 కు పంపండి."
    ),
    "dump_qr_error": "చెల్లింపు QR చూపించడం సాధ్యం కాలేదు. దయచేసి /dump పంపి మళ్లీ ప్రయత్నించండి.",
    "dump_unavailable": "డంప్ యాక్సెస్ సమాచారం తాత్కాలికంగా అందుబాటులో లేదు.",
    "dump_menu_unavailable": "చెల్లింపు మెనూ తాత్కాలికంగా అందుబాటులో లేదు.",
    "select_language": "🌐 మీ భాషను ఎంచుకోండి:",
    "language_saved": "✅ ఎంచుకున్న భాష: {language}",
    "confirm": "✅ ఖరారు చేయండి",
    "settings_title": "⚙️ యూజర్ సెట్టింగ్‌లు",
}

TRANSLATIONS["kn"] = {
    "welcome": "🌟 {mention}, ನಾನು ಒಬ್ಬ ಟೆರಾಬಾಕ್ಸ್ ಡೌನ್‌ಲೋಡರ್ ಬಾಟ್. ಯಾವುದೇ ಟೆರಾಬಾಕ್ಸ್ ಲಿಂಕ್ ಅನ್ನು ನನಗೆ ಕಳುಹಿಸಿ, ನಾನು ಕೆಲವೇ ಸೆಕೆಂಡುಗಳಲ್ಲಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ ನಿಮಗೆ ಕಳುಹಿಸುತ್ತೇನೆ ✨.",
    "must_join": "ನನ್ನನ್ನು ಬಳಸಲು ನೀವು ನನ್ನ ಚಾನೆಲ್ ಅನ್ನು ಸೇರಬೇಕು.",
    "cooldown": "ಎಪಿಐ ಅಭಿವೃದ್ಧಿಯಲ್ಲಿದೆ. ದುರ್ಬಳಕೆ ಕಡಿಮೆ ಮಾಡಲು ನೀವು {remaining} ಸೆಕೆಂಡುಗಳು ಕಾಯಬೇಕು.",
    "invalid_link": "ದಯವಿಟ್ಟು ಮಾನ್ಯವಾದ ಟೆರಾಬಾಕ್ಸ್ ಲಿಂಕ್ ನೀಡಿ.",
    "sending_media": "ನಿಮಗೆ ಮಾಧ್ಯಮ ಕಳುಹಿಸುತ್ತಿದ್ದೇನೆ...🤤",
    "download_failed": (
        "ಡೌನ್‌ಲೋಡ್ ವಿಫಲವಾಗಿದೆ ❌\n\n"
        "ಕಾರಣ: ಲಿಂಕ್ ಮುರಿದಿರಬಹುದು ಅಥವಾ ಅದು ಫೋಲ್ಡರ್ ಲಿಂಕ್ ಆಗಿರಬಹುದು.\n"
        "ಫೈಲ್ ಲಿಂಕ್‌ಗಳು ಮಾತ್ರ ಬೆಂಬಲಿತವಾಗಿವೆ."
    ),
    "file_deleted_warning": "⚠️ ಈ ಫೈಲ್ 10 ನಿಮಿಷಗಳಲ್ಲಿ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಅಳಿಸಲ್ಪಡುತ್ತದೆ. ಉಳಿಸಲು ಫಾರ್ವರ್ಡ್ ಮಾಡಿ.",
    "no_videos": "ಇನ್ನೂ ಯಾವುದೇ ವೀಡಿಯೊಗಳು ಸೂಚ್ಯಂಕಗೊಂಡಿಲ್ಲ. ಸೂಚಿಯನ್ನು ನಿರ್ಮಿಸಲು ಮಾಲೀಕರು /refresh ಬಳಸಬಹುದು.",
    "mongo_missing": "MongoDB ಕಾನ್ಫಿಗರ್ ಮಾಡಲಾಗಿಲ್ಲ.",
    "search_usage": "ಬಳಕೆ: /search <1 ರಿಂದ 3 ಕೀವರ್ಡ್‌ಗಳು>",
    "search_no_results": "ನೀಡಿದ ಎಲ್ಲಾ ಕೀವರ್ಡ್‌ಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗುವ ಯಾವುದೇ ಫೈಲ್ ಕಂಡುಬಂದಿಲ್ಲ.",
    "search_unavailable": "ಹುಡುಕಾಟ ತಾತ್ಕಾಲಿಕವಾಗಿ ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    "search_expired": "ಈ ಹುಡುಕಾಟದ ಅವಧಿ ಮುಗಿದಿದೆ. /search ಅನ್ನು ಮತ್ತೆ ಕಳುಹಿಸಿ.",
    "search_not_yours": "ಈ ಹುಡುಕಾಟ ಇನ್ನೊಬ್ಬ ಬಳಕೆದಾರರದು.",
    "search_none_left": "ಈಗ ಯಾವುದೇ ಹೊಂದಿಕೆಯಾಗುವ ಫೈಲ್‌ಗಳಿಲ್ಲ.",
    "search_send_failed": "ಈ ಫೈಲ್ ಕಳುಹಿಸಲು ವಿಫಲವಾಗಿದೆ. ಬಹುಶಃ ಅದನ್ನು ಮೂಲ ಚಾನೆಲ್‌ನಿಂದ ತೆಗೆದುಹಾಕಲಾಗಿದೆ.",
    "search_header": "🔎 ಹುಡುಕಾಟ: {keywords}\n{count} ಹೊಂದಿಕೆಯಾಗುವ ಫೈಲ್‌ಗಳು ದೊರೆತಿವೆ. ಕೆಳಗೆ ಫೈಲ್ ಹೆಸರನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
    "search_sending": "ಫೈಲ್ ಕಳುಹಿಸುತ್ತಿದ್ದೇನೆ...",
    "search_file_unavailable": "ಈ ಫೈಲ್ ಈಗ ಲಭ್ಯವಿಲ್ಲ.",
    "dump_caption": (
        "💾 ಶಾಶ್ವತ ಡಂಪ್ ಚಾನೆಲ್ ಪ್ರವೇಶ\n\n"
        "ಇಡೀ ಡಂಪ್ ಚಾನೆಲ್‌ನ ಶಾಶ್ವತ ಪ್ರವೇಶವನ್ನು ಖರೀದಿಸಿ.\n\n"
        "• Binance: 1.5 USDT ಮಾತ್ರ\n"
        "• UPI: ₹200 ಮಾತ್ರ\n\n"
        "ಕೆಳಗೆ ನಿಮ್ಮ ಪಾವತಿ ವಿಧಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ. ಪಾವತಿಸಿದ ನಂತರ, "
        "ಪರಿಶೀಲನೆಗಾಗಿ ಪಾವತಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು @rtx5069 ಗೆ ಕಳುಹಿಸಿ."
    ),
    "dump_qr_binance": (
        "Binance ಪಾವತಿ\n\n"
        "ಮೊತ್ತ: 1.5 USDT ಮಾತ್ರ\n\n"
        "Binance ಆಪ್‌ನಿಂದ ಈ QR ಅನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ. ಪಾವತಿಸಿದ ನಂತರ, "
        "ಪರಿಶೀಲನೆಗಾಗಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು @rtx5069 ಗೆ ಕಳುಹಿಸಿ."
    ),
    "dump_qr_upi": (
        "UPI ಪಾವತಿ\n\n"
        "ಮೊತ್ತ: ₹200 ಮಾತ್ರ\n\n"
        "ಯಾವುದೇ UPI ಆಪ್‌ನಿಂದ ಈ QR ಅನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ. ಪಾವತಿಸಿದ ನಂತರ, "
        "ಪರಿಶೀಲನೆಗಾಗಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು @rtx5069 ಗೆ ಕಳುಹಿಸಿ."
    ),
    "dump_qr_error": "ಪಾವತಿ QR ತೋರಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು /dump ಕಳುಹಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    "dump_unavailable": "ಡಂಪ್ ಪ್ರವೇಶ ಮಾಹಿತಿ ತಾತ್ಕಾಲಿಕವಾಗಿ ಲಭ್ಯವಿಲ್ಲ.",
    "dump_menu_unavailable": "ಪಾವತಿ ಮೆನು ತಾತ್ಕಾಲಿಕವಾಗಿ ಲಭ್ಯವಿಲ್ಲ.",
    "select_language": "🌐 ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
    "language_saved": "✅ ಆಯ್ಕೆ ಮಾಡಿದ ಭಾಷೆ: {language}",
    "confirm": "✅ ದೃಢೀಕರಿಸಿ",
    "settings_title": "⚙️ ಬಳಕೆದಾರರ ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
}

TRANSLATIONS["ml"] = {
    "welcome": "🌟 {mention}, ഞാൻ ഒരു ടെറാബോക്സ് ഡൗൺലോഡർ ബോട്ട് ആണ്. ഏതെങ്കിലും ടെറാബോക്സ് ലിങ്ക് എനിക്ക് അയയ്ക്കുക, ഞാൻ ചില നിമിഷങ്ങൾക്കുള്ളിൽ ഡൗൺലോഡ് ചെയ്ത് നിങ്ങൾക്ക് അയയ്ക്കും ✨.",
    "must_join": "എന്നെ ഉപയോഗിക്കാൻ നിങ്ങൾ എന്റെ ചാനലിൽ ചേർന്നിരിക്കണം.",
    "cooldown": "എപിഐ വികസനത്തിലാണ്. ദുരുപയോഗം കുറയ്ക്കാൻ നിങ്ങൾ {remaining} സെക്കൻഡ് കാത്തിരിക്കണം.",
    "invalid_link": "ദയവായി സാധുവായ ഒരു ടെറാബോക്സ് ലിങ്ക് നൽകുക.",
    "sending_media": "നിങ്ങൾക്ക് മീഡിയ അയയ്ക്കുന്നു...🤤",
    "download_failed": (
        "ഡൗൺലോഡ് പരാജയപ്പെട്ടു ❌\n\n"
        "കാരണം: ലിങ്ക് തകരാറുള്ളതാകാം അല്ലെങ്കിൽ അത് ഒരു ഫോൾഡർ ലിങ്ക് ആകാം.\n"
        "ഫയൽ ലിങ്കുകൾ മാത്രമേ പിന്തുണയ്ക്കൂ."
    ),
    "file_deleted_warning": "⚠️ ഈ ഫയൽ 10 മിനിറ്റിനുള്ളിൽ സ്വയമേവ നീക്കം ചെയ്യപ്പെടും. സംരക്ഷിക്കാൻ ഫോർവേഡ് ചെയ്യുക.",
    "no_videos": "ഇതുവരെ ഒരു വീഡിയോയും സൂചികയിലാക്കിയിട്ടില്ല. സൂചിക നിർമ്മിക്കാൻ ഉടമസ്ഥൻ /refresh ഉപയോഗിക്കാം.",
    "mongo_missing": "MongoDB കോൺഫിഗർ ചെയ്തിട്ടില്ല.",
    "search_usage": "ഉപയോഗം: /search <1 മുതൽ 3 വരെ കീവേഡുകൾ>",
    "search_no_results": "നൽകിയ എല്ലാ കീവേഡുകളും ചേരുന്ന ഫയലുകളൊന്നും കണ്ടെത്തിയില്ല.",
    "search_unavailable": "തിരച്ചിൽ താൽക്കാലികമായി ലഭ്യമല്ല. ദയവായി വീണ്ടും ശ്രമിക്കുക.",
    "search_expired": "ഈ തിരച്ചിൽ കാലഹരണപ്പെട്ടു. /search വീണ്ടും അയയ്ക്കുക.",
    "search_not_yours": "ഈ തിരച്ചിൽ മറ്റൊരു ഉപയോക്താവിന്റേതാണ്.",
    "search_none_left": "ഇപ്പോൾ ചേരുന്ന ഫയലുകളൊന്നുമില്ല.",
    "search_send_failed": "ഈ ഫയൽ അയയ്ക്കാൻ കഴിഞ്ഞില്ല. അത് ഉറവിട ചാനലിൽ നിന്ന് നീക്കം ചെയ്യപ്പെട്ടിരിക്കാം.",
    "search_header": "🔎 തിരച്ചിൽ: {keywords}\n{count} ചേരുന്ന ഫയലുകൾ കണ്ടെത്തി. താഴെ നിന്ന് ഫയലിന്റെ പേര് തിരഞ്ഞെടുക്കുക.",
    "search_sending": "ഫയൽ അയയ്ക്കുന്നു...",
    "search_file_unavailable": "ഈ ഫയൽ ഇപ്പോൾ ലഭ്യമല്ല.",
    "dump_caption": (
        "💾 സ്ഥിരകാല ഡംപ് ചാനൽ ആക്‌സസ്സ്\n\n"
        "മുഴുവൻ ഡംപ് ചാനലിന്റെയും സ്ഥിരകാല ആക്‌സസ്സ് വാങ്ങുക.\n\n"
        "• Binance: 1.5 USDT മാത്രം\n"
        "• UPI: ₹200 മാത്രം\n\n"
        "താഴെ നിങ്ങളുടെ പണമടയ്ക്കൽ രീതി തിരഞ്ഞെടുക്കുക. പണമടച്ച ശേഷം, "
        "സ്ഥിരീകരണത്തിനായി സ്ക്രീൻഷോട്ട് @rtx5069 ന് അയയ്ക്കുക."
    ),
    "dump_qr_binance": (
        "Binance പണമടയ്ക്കൽ\n\n"
        "തുക: 1.5 USDT മാത്രം\n\n"
        "Binance ആപ്പ് ഉപയോഗിച്ച് ഈ QR സ്കാൻ ചെയ്യുക. പണമടച്ച ശേഷം, "
        "സ്ഥിരീകരണത്തിനായി സ്ക്രീൻഷോട്ട് @rtx5069 ന് അയയ്ക്കുക."
    ),
    "dump_qr_upi": (
        "UPI പണമടയ്ക്കൽ\n\n"
        "തുക: ₹200 മാത്രം\n\n"
        "ഏതെങ്കിലും UPI ആപ്പ് ഉപയോഗിച്ച് ഈ QR സ്കാൻ ചെയ്യുക. പണമടച്ച ശേഷം, "
        "സ്ഥിരീകരണത്തിനായി സ്ക്രീൻഷോട്ട് @rtx5069 ന് അയയ്ക്കുക."
    ),
    "dump_qr_error": "പണമടയ്ക്കൽ QR കാണിക്കാൻ കഴിഞ്ഞില്ല. ദയവായി /dump അയച്ച് വീണ്ടും ശ്രമിക്കുക.",
    "dump_unavailable": "ഡംപ് ആക്‌സസ്സ് വിവരം താൽക്കാലികമായി ലഭ്യമല്ല.",
    "dump_menu_unavailable": "പണമടയ്ക്കൽ മെനു താൽക്കാലികമായി ലഭ്യമല്ല.",
    "select_language": "🌐 നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക:",
    "language_saved": "✅ തിരഞ്ഞെടുത്ത ഭാഷ: {language}",
    "confirm": "✅ സ്ഥിരീകരിക്കുക",
    "settings_title": "⚙️ ഉപയോക്തൃ ക്രമീകരണങ്ങൾ",
}

TRANSLATIONS["ur"] = {
    "welcome": "🌟 {mention}، میں ایک ٹیرا باکس ڈاؤن لوڈر بوٹ ہوں۔ مجھے کوئی بھی ٹیرا باکس لنک بھیجیں، میں اسے چند سیکنڈ میں ڈاؤن لوڈ کر کے آپ کو بھیج دوں گا ✨۔",
    "must_join": "مجھے استعمال کرنے کے لیے آپ کو میرے چینل میں شامل ہونا ضروری ہے۔",
    "cooldown": "اے پی آی ترقی کے مرحلے میں ہے۔ غلط استعمال کم کرنے کے لیے آپ کو {remaining} سیکنڈ انتظار کرنا ہوگا۔",
    "invalid_link": "براہ کرم ایک درست ٹیرا باکس لنک دیں۔",
    "sending_media": "آپ کو میڈیا بھیج رہا ہوں...🤤",
    "download_failed": (
        "ڈاؤن لوڈ ناکام ❌\n\n"
        "وجہ: لنک خراب ہو سکتا ہے یا یہ فولڈر لنک ہے۔\n"
        "صرف فائل لنکس سپورٹڈ ہیں۔"
    ),
    "file_deleted_warning": "⚠️ یہ فائل 10 منٹ میں خود بخود حذف ہو جائے گی۔ محفوظ کرنے کے لیے فارورڈ کریں۔",
    "no_videos": "ابھی کوئی ویڈیو انڈیکس نہیں ہوئی۔ اشاریہ بنانے کے لیے مالک /refresh استعمال کر سکتا ہے۔",
    "mongo_missing": "MongoDB ترتیب نہیں دیا گیا۔",
    "search_usage": "استعمال: /search <1 سے 3 کی ورڈز>",
    "search_no_results": "دی گئی تمام کی ورڈز سے ملنے والی کوئی فائل نہیں ملی۔",
    "search_unavailable": "تلاش عارضی طور پر دستیاب نہیں۔ براہ کرم دوبارہ کوشش کریں۔",
    "search_expired": "یہ تلاش ختم ہو گئی ہے۔ /search دوبارہ بھیجیں۔",
    "search_not_yours": "یہ تلاش کسی اور صارف کی ہے۔",
    "search_none_left": "اب کوئی ملنے والی فائل دستیاب نہیں۔",
    "search_send_failed": "یہ فائل بھیجنے میں ناکامی۔ ممکن ہے اسے سورس چینل سے ہٹا دیا گیا ہو۔",
    "search_header": "🔎 تلاش: {keywords}\n{count} ملنے والی فائلیں ملیں۔ نیچے سے فائل کا نام منتخب کریں۔",
    "search_sending": "فائل بھیج رہا ہوں...",
    "search_file_unavailable": "یہ فائل اب دستیاب نہیں۔",
    "dump_caption": (
        "💾 مستقل ڈمپ چینل تک رسائی\n\n"
        "پورے ڈمپ چینل تک مستقل رسائی حاصل کریں۔\n\n"
        "• Binance: صرف 1.5 USDT\n"
        "• UPI: صرف ₹200\n\n"
        "نیچے اپنی ادائیگی کا طریقہ منتخب کریں۔ ادائیگی کے بعد، تصدیق کے "
        "لیے ادائیگی کا اسکرین شاٹ @rtx5069 کو بھیجیں۔"
    ),
    "dump_qr_binance": (
        "Binance ادائیگی\n\n"
        "رقم: صرف 1.5 USDT\n\n"
        "Binance ایپ سے یہ QR سکین کریں۔ ادائیگی کے بعد، تصدیق کے لیے "
        "اسکرین شاٹ @rtx5069 کو بھیجیں۔"
    ),
    "dump_qr_upi": (
        "UPI ادائیگی\n\n"
        "رقم: صرف ₹200\n\n"
        "کسی بھی UPI ایپ سے یہ QR سکین کریں۔ ادائیگی کے بعد، تصدیق کے لیے "
        "اسکرین شاٹ @rtx5069 کو بھیجیں۔"
    ),
    "dump_qr_error": "ادائیگی کا QR دکھایا نہیں جا سکا۔ براہ کرم /dump بھیج کر دوبارہ کوشش کریں۔",
    "dump_unavailable": "ڈمپ تک رسائی کی معلومات عارضی طور پر دستیاب نہیں۔",
    "dump_menu_unavailable": "ادائیگی کا مینو عارضی طور پر دستیاب نہیں۔",
    "select_language": "🌐 اپنی زبان منتخب کریں:",
    "language_saved": "✅ منتخب زبان: {language}",
    "confirm": "✅ تصدیق کریں",
    "settings_title": "⚙️ صارف سیٹنگز",
}

TRANSLATIONS["pa"] = {
    "welcome": "🌟 {mention}, ਮੈਂ ਇੱਕ ਟੈਰਾਬਾਕਸ ਡਾਊਨਲੋਡਰ ਬੋਟ ਹਾਂ। ਮੈਨੂੰ ਕੋਈ ਵੀ ਟੈਰਾਬਾਕਸ ਲਿੰਕ ਭੇਜੋ, ਮੈਂ ਇਸਨੂੰ ਕੁਝ ਸਕਿੰਟਾਂ ਵਿੱਚ ਡਾਊਨਲੋਡ ਕਰਕੇ ਤੁਹਾਨੂੰ ਭੇਜ ਦਵਾਂਗਾ ✨।",
    "must_join": "ਮੈਨੂੰ ਵਰਤਣ ਲਈ ਤੁਹਾਨੂੰ ਮੇਰੇ ਚੈਨਲ ਵਿੱਚ ਸ਼ਾਮਲ ਹੋਣਾ ਹੋਵੇਗਾ।",
    "cooldown": "ਏਪੀਆਈ ਵਿਕਾਸ ਅਧੀਨ ਹੈ। ਦੁਰਵਿਅਹਾਰ ਘਟਾਉਣ ਲਈ ਤੁਹਾਨੂੰ {remaining} ਸਕਿੰਟ ਉਡੀਕ ਕਰਨੀ ਪਵੇਗੀ।",
    "invalid_link": "ਕਿਰਪਾ ਕਰਕੇ ਇੱਕ ਵੈਧ ਟੈਰਾਬਾਕਸ ਲਿੰਕ ਦਿਓ।",
    "sending_media": "ਤੁਹਾਨੂੰ ਮੀਡੀਆ ਭੇਜ ਰਿਹਾ ਹਾਂ...🤤",
    "download_failed": (
        "ਡਾਊਨਲੋਡ ਅਸਫਲ ❌\n\n"
        "ਕਾਰਨ: ਲਿੰਕ ਟੁੱਟਿਆ ਹੋ ਸਕਦਾ ਹੈ ਜਾਂ ਇਹ ਇੱਕ ਫੋਲਡਰ ਲਿੰਕ ਹੈ।\n"
        "ਸਿਰਫ਼ ਫਾਈਲ ਲਿੰਕ ਸਮਰਥਿਤ ਹਨ।"
    ),
    "file_deleted_warning": "⚠️ ਇਹ ਫਾਈਲ 10 ਮਿੰਟਾਂ ਵਿੱਚ ਆਪਣੇ ਆਪ ਮਿਟ ਜਾਵੇਗੀ। ਸੰਭਾਲਣ ਲਈ ਫਾਰਵਰਡ ਕਰੋ।",
    "no_videos": "ਹਾਲੇ ਕੋਈ ਵੀਡੀਓ ਇੰਡੈਕਸ ਨਹੀਂ ਹੋਈ। ਸੂਚੀ ਬਣਾਉਣ ਲਈ ਮਾਲਕ /refresh ਵਰਤ ਸਕਦਾ ਹੈ।",
    "mongo_missing": "MongoDB ਕੌਨਫਿਗਰ ਨਹੀਂ ਹੈ।",
    "search_usage": "ਵਰਤੋਂ: /search <1 ਤੋਂ 3 ਕੀਵਰਡ>",
    "search_no_results": "ਦਿੱਤੇ ਗਏ ਸਾਰੇ ਕੀਵਰਡਾਂ ਨਾਲ ਮਿਲਦੀ ਕੋਈ ਫਾਈਲ ਨਹੀਂ ਮਿਲੀ।",
    "search_unavailable": "ਖੋਜ ਅਸਥਾਈ ਤੌਰ 'ਤੇ ਉਪਲਬਧ ਨਹੀਂ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
    "search_expired": "ਇਹ ਖੋਜ ਸਮਾਪਤ ਹੋ ਗਈ ਹੈ। /search ਦੁਬਾਰਾ ਭੇਜੋ।",
    "search_not_yours": "ਇਹ ਖੋਜ ਕਿਸੇ ਹੋਰ ਵਰਤੋਂਕਾਰ ਦੀ ਹੈ।",
    "search_none_left": "ਹੁਣ ਕੋਈ ਮਿਲਦੀ ਫਾਈਲ ਉਪਲਬਧ ਨਹੀਂ।",
    "search_send_failed": "ਇਹ ਫਾਈਲ ਭੇਜਣ ਵਿੱਚ ਅਸਫਲ। ਸ਼ਾਇਦ ਇਸਨੂੰ ਸਰੋਤ ਚੈਨਲ ਤੋਂ ਹਟਾ ਦਿੱਤਾ ਗਿਆ ਹੈ।",
    "search_header": "🔎 ਖੋਜ: {keywords}\n{count} ਮਿਲਦੀਆਂ ਫਾਈਲਾਂ ਮਿਲੀਆਂ। ਹੇਠੋਂ ਫਾਈਲ ਦਾ ਨਾਮ ਚੁਣੋ।",
    "search_sending": "ਫਾਈਲ ਭੇਜ ਰਿਹਾ ਹਾਂ...",
    "search_file_unavailable": "ਇਹ ਫਾਈਲ ਹੁਣ ਉਪਲਬਧ ਨਹੀਂ।",
    "dump_caption": (
        "💾 ਸਥਾਈ ਡੰਪ ਚੈਨਲ ਪਹੁੰਚ\n\n"
        "ਪੂਰੇ ਡੰਪ ਚੈਨਲ ਦੀ ਸਥਾਈ ਪਹੁੰਚ ਖਰੀਦੋ।\n\n"
        "• Binance: ਸਿਰਫ਼ 1.5 USDT\n"
        "• UPI: ਸਿਰਫ਼ ₹200\n\n"
        "ਹੇਠਾਂ ਆਪਣਾ ਭੁਗਤਾਨ ਤਰੀਕਾ ਚੁਣੋ। ਭੁਗਤਾਨ ਤੋਂ ਬਾਅਦ, ਤਸਦੀਕ ਲਈ "
        "ਭੁਗਤਾਨ ਸਕਰੀਨਸ਼ਾਟ @rtx5069 ਨੂੰ ਭੇਜੋ।"
    ),
    "dump_qr_binance": (
        "Binance ਭੁਗਤਾਨ\n\n"
        "ਰਕਮ: ਸਿਰਫ਼ 1.5 USDT\n\n"
        "Binance ਐਪ ਨਾਲ ਇਹ QR ਸਕੈਨ ਕਰੋ। ਭੁਗਤਾਨ ਤੋਂ ਬਾਅਦ, ਤਸਦੀਕ ਲਈ "
        "ਸਕਰੀਨਸ਼ਾਟ @rtx5069 ਨੂੰ ਭੇਜੋ।"
    ),
    "dump_qr_upi": (
        "UPI ਭੁਗਤਾਨ\n\n"
        "ਰਕਮ: ਸਿਰਫ਼ ₹200\n\n"
        "ਕਿਸੇ ਵੀ UPI ਐਪ ਨਾਲ ਇਹ QR ਸਕੈਨ ਕਰੋ। ਭੁਗਤਾਨ ਤੋਂ ਬਾਅਦ, ਤਸਦੀਕ ਲਈ "
        "ਸਕਰੀਨਸ਼ਾਟ @rtx5069 ਨੂੰ ਭੇਜੋ।"
    ),
    "dump_qr_error": "ਭੁਗਤਾਨ QR ਨਹੀਂ ਦਿਖਾਇਆ ਜਾ ਸਕਿਆ। ਕਿਰਪਾ ਕਰਕੇ /dump ਭੇਜ ਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
    "dump_unavailable": "ਡੰਪ ਪਹੁੰਚ ਜਾਣਕਾਰੀ ਅਸਥਾਈ ਤੌਰ 'ਤੇ ਉਪਲਬਧ ਨਹੀਂ।",
    "dump_menu_unavailable": "ਭੁਗਤਾਨ ਮੀਨੂ ਅਸਥਾਈ ਤੌਰ 'ਤੇ ਉਪਲਬਧ ਨਹੀਂ।",
    "select_language": "🌐 ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ:",
    "language_saved": "✅ ਚੁਣੀ ਹੋਈ ਭਾਸ਼ਾ: {language}",
    "confirm": "✅ ਪੁਸ਼ਟੀ ਕਰੋ",
    "settings_title": "⚙️ ਵਰਤੋਂਕਾਰ ਸੈਟਿੰਗਾਂ",
}

TRANSLATIONS["gu"] = {
    "welcome": "🌟 {mention}, હું એક ટેરાબોક્સ ડાઉનલોડર બોટ છું. મને કોઈપણ ટેરાબોક્સ લિંક મોકલો, હું તેને થોડી સેકંડોમાં ડાઉનલોડ કરીને તમને મોકલી આપીશ ✨.",
    "must_join": "મને વાપરવા માટે તમારે મારા ચેનલમાં જોડાવું પડશે.",
    "cooldown": "એપીઆઈ વિકાસમાન છે. દુરુપયોગ ઘટાડવા માટે તમારે {remaining} સેકંડ રાહ જોવી પડશે.",
    "invalid_link": "કૃપા કરીને માન્ય ટેરાબોક્સ લિંક આપો.",
    "sending_media": "તમને મીડિયા મોકલી રહ્યો છું...🤤",
    "download_failed": (
        "ડાઉનલોડ નિષ્ફળ ❌\n\n"
        "કારણ: લિંક તૂટેલી હોઈ શકે છે અથવા તે ફોલ્ડર લિંક છે.\n"
        "ફક્ત ફાઇલ લિંક્સ સપોર્ટેડ છે."
    ),
    "file_deleted_warning": "⚠️ આ ફાઇલ 10 મિનિટમાં આપમેળે કાઢી નાખવામાં આવશે. સાચવવા ફોરવર્ડ કરો.",
    "no_videos": "હજુ કોઈ વિડિયો અનુક્રમણિકામાં નથી. અનુક્રમણિકા બનાવવા માલિક /refresh વાપરી શકે છે.",
    "mongo_missing": "MongoDB કન્ફિગર કરેલું નથી.",
    "search_usage": "વપરાશ: /search <1 થી 3 કીવર્ડ>",
    "search_no_results": "આપેલા તમામ કીવર્ડ સાથે મેળ ખાતી કોઈ ફાઇલ મળી નથી.",
    "search_unavailable": "શોધ કામતરી રીતે અનુપલબ્ધ છે. કૃપા કરીને ફરી પ્રયાસ કરો.",
    "search_expired": "આ શોધ સમાપ્ત થઈ ગઈ છે. /search ફરી મોકલો.",
    "search_not_yours": "આ શોધ બીજા વપરાશકર્તાની છે.",
    "search_none_left": "હવે કોઈ મેળ ખાતી ફાઇલ ઉપલબ્ધ નથી.",
    "search_send_failed": "આ ફાઇલ મોકલવામાં નિષ્ફળ. કદાચ તેને સ્ત્રોત ચેનલમાંથી દૂર કરવામાં આવી છે.",
    "search_header": "🔎 શોધ: {keywords}\n{count} મેળ ખાતી ફાઇલો મળી. નીચેથી ફાઇલનું નામ પસંદ કરો.",
    "search_sending": "ફાઇલ મોકલી રહ્યો છું...",
    "search_file_unavailable": "આ ફાઇલ હવે ઉપલબ્ધ નથી.",
    "dump_caption": (
        "💾 કાયમી ડમ્પ ચેનલ ઍક્સેસ\n\n"
        "આખા ડમ્પ ચેનલની કાયમી ઍક્સેસ ખરીદો.\n\n"
        "• Binance: ફક્ત 1.5 USDT\n"
        "• UPI: ફક્ત ₹200\n\n"
        "નીચે તમારી ચુકવણી પદ્ધતિ પસંદ કરો. ચુકવણી પછી, ચકાસણી માટે "
        "ચુકવણી સ્ક્રીનશોટ @rtx5069 ને મોકલો."
    ),
    "dump_qr_binance": (
        "Binance ચુકવણી\n\n"
        "રકમ: ફક્ત 1.5 USDT\n\n"
        "Binance એપથી આ QR સ્કેન કરો. ચુકવણી પછી, ચકાસણી માટે "
        "સ્ક્રીનશોટ @rtx5069 ને મોકલો."
    ),
    "dump_qr_upi": (
        "UPI ચુકવણી\n\n"
        "રકમ: ફક્ત ₹200\n\n"
        "કોઈપણ UPI એપથી આ QR સ્કેન કરો. ચુકવણી પછી, ચકાસણી માટે "
        "સ્ક્રીનશોટ @rtx5069 ને મોકલો."
    ),
    "dump_qr_error": "ચુકવણી QR બતાવવામાં નિષ્ફળ. કૃપા કરીને /dump મોકલીને ફરી પ્રયાસ કરો.",
    "dump_unavailable": "ડમ્પ ઍક્સેસ માહિતી કામતરી રીતે અનુપલબ્ધ છે.",
    "dump_menu_unavailable": "ચુકવણી મેનુ કામતરી રીતે અનુપલબ્ધ છે.",
    "select_language": "🌐 તમારી ભાષા પસંદ કરો:",
    "language_saved": "✅ પસંદ કરેલી ભાષા: {language}",
    "confirm": "✅ પુષ્ટિ કરો",
    "settings_title": "⚙️ વપરાશકર્તા સેટિંગ્સ",
}

TRANSLATIONS["es"] = {
    "welcome": "🌟 {mention}, soy un bot descargador de Terabox. Envíame cualquier enlace de Terabox, lo descargaré en segundos y te lo enviaré ✨.",
    "must_join": "Debes unirte a mi canal para usarme.",
    "cooldown": "La API está en desarrollo. Para reducir el abuso debes esperar {remaining}s.",
    "invalid_link": "Por favor, proporciona un enlace válido de Terabox.",
    "sending_media": "Enviándote el medio...🤤",
    "download_failed": (
        "Descarga fallida ❌\n\n"
        "Razón: el enlace puede estar roto o es de una carpeta.\n"
        "Solo se admiten enlaces de archivos."
    ),
    "file_deleted_warning": "⚠️ Este archivo se eliminará automáticamente en 10 minutos. Reenvíalo para guardarlo.",
    "no_videos": "Aún no hay vídeos indexados. El propietario puede usar /refresh para crear el índice.",
    "mongo_missing": "MongoDB no está configurado.",
    "search_usage": "Uso: /search <1 a 3 palabras clave>",
    "search_no_results": "No se encontró ningún archivo que coincida con todas las palabras clave.",
    "search_unavailable": "La búsqueda no está disponible temporalmente. Inténtalo de nuevo.",
    "search_expired": "Esta búsqueda ha expirado. Envía /search de nuevo.",
    "search_not_yours": "Esta búsqueda pertenece a otro usuario.",
    "search_none_left": "Ya no hay archivos coincidentes disponibles.",
    "search_send_failed": "No se pudo enviar este archivo. Puede que haya sido eliminado del canal de origen.",
    "search_header": "🔎 Búsqueda: {keywords}\nSe encontraron {count} archivos coincidentes. Selecciona un nombre abajo.",
    "search_sending": "Enviando archivo...",
    "search_file_unavailable": "Este archivo ya no está disponible.",
    "dump_caption": (
        "💾 Acceso permanente al canal de descargas\n\n"
        "Compra acceso permanente a todo el canal.\n\n"
        "• Binance: solo 1.5 USDT\n"
        "• UPI: solo ₹200\n\n"
        "Elige tu método de pago abajo. Tras pagar, envía la captura del "
        "pago a @rtx5069 para verificarlo."
    ),
    "dump_qr_binance": (
        "Pago con Binance\n\n"
        "Importe: solo 1.5 USDT\n\n"
        "Escanea este código QR con la app de Binance. Tras pagar, envía "
        "la captura a @rtx5069 para verificarlo."
    ),
    "dump_qr_upi": (
        "Pago por UPI\n\n"
        "Importe: solo ₹200\n\n"
        "Escanea este código QR con cualquier app de UPI. Tras pagar, "
        "envía la captura a @rtx5069 para verificarlo."
    ),
    "dump_qr_error": "No se pudo mostrar el QR de pago. Envía /dump e inténtalo de nuevo.",
    "dump_unavailable": "La información de acceso al canal no está disponible temporalmente.",
    "dump_menu_unavailable": "El menú de pago no está disponible temporalmente.",
    "select_language": "🌐 Elige tu idioma:",
    "language_saved": "✅ Idioma establecido: {language}",
    "confirm": "✅ Confirmar",
    "settings_title": "⚙️ Ajustes de usuario",
}

TRANSLATIONS["fr"] = {
    "welcome": "🌟 {mention}, je suis un bot téléchargeur Terabox. Envoyez-moi n'importe quel lien Terabox, je le téléchargerai en quelques secondes et vous l'enverrai ✨.",
    "must_join": "Vous devez rejoindre mon canal pour m'utiliser.",
    "cooldown": "L'API est en cours de développement. Pour réduire les abus, vous devez attendre {remaining}s.",
    "invalid_link": "Veuillez fournir un lien Terabox valide.",
    "sending_media": "Envoi du média...🤤",
    "download_failed": (
        "Échec du téléchargement ❌\n\n"
        "Raison : le lien est peut-être cassé ou c'est un lien de dossier.\n"
        "Seuls les liens de fichiers sont pris en charge."
    ),
    "file_deleted_warning": "⚠️ Ce fichier sera automatiquement supprimé dans 10 minutes. Transférez-le pour le conserver.",
    "no_videos": "Aucune vidéo indexée pour le moment. Le propriétaire peut utiliser /refresh pour créer l'index.",
    "mongo_missing": "MongoDB n'est pas configuré.",
    "search_usage": "Utilisation : /search <1 à 3 mots-clés>",
    "search_no_results": "Aucun fichier correspondant à tous les mots-clés fournis n'a été trouvé.",
    "search_unavailable": "La recherche est temporairement indisponible. Veuillez réessayer.",
    "search_expired": "Cette recherche a expiré. Envoyez /search à nouveau.",
    "search_not_yours": "Cette recherche appartient à un autre utilisateur.",
    "search_none_left": "Plus aucun fichier correspondant n'est disponible.",
    "search_send_failed": "Échec de l'envoi de ce fichier. Il a peut-être été supprimé du canal source.",
    "search_header": "🔎 Recherche : {keywords}\n{count} fichiers correspondants trouvés. Sélectionnez un nom ci-dessous.",
    "search_sending": "Envoi du fichier...",
    "search_file_unavailable": "Ce fichier n'est plus disponible.",
    "dump_caption": (
        "💾 Accès permanent au canal de stockage\n\n"
        "Achetez un accès permanent à l'ensemble du canal.\n\n"
        "• Binance : seulement 1,5 USDT\n"
        "• UPI : seulement 200 ₹\n\n"
        "Choisissez votre moyen de paiement ci-dessous. Après paiement, "
        "envoyez la capture d'écran à @rtx5069 pour vérification."
    ),
    "dump_qr_binance": (
        "Paiement Binance\n\n"
        "Montant : seulement 1,5 USDT\n\n"
        "Scannez ce QR avec l'application Binance. Après paiement, envoyez "
        "la capture d'écran à @rtx5069 pour vérification."
    ),
    "dump_qr_upi": (
        "Paiement UPI\n\n"
        "Montant : seulement 200 ₹\n\n"
        "Scannez ce QR avec n'importe quelle application UPI. Après "
        "paiement, envoyez la capture d'écran à @rtx5069 pour vérification."
    ),
    "dump_qr_error": "Impossible d'afficher le QR de paiement. Envoyez /dump et réessayez.",
    "dump_unavailable": "Les informations d'accès au canal sont temporairement indisponibles.",
    "dump_menu_unavailable": "Le menu de paiement est temporairement indisponible.",
    "select_language": "🌐 Choisissez votre langue :",
    "language_saved": "✅ Langue définie : {language}",
    "confirm": "✅ Confirmer",
    "settings_title": "⚙️ Paramètres utilisateur",
}

TRANSLATIONS["de"] = {
    "welcome": "🌟 {mention}, ich bin ein Terabox-Downloader-Bot. Sende mir einen beliebigen Terabox-Link, ich lade ihn in wenigen Sekunden herunter und schicke ihn dir ✨.",
    "must_join": "Du musst meinem Kanal beitreten, um mich zu nutzen.",
    "cooldown": "Die API ist in Entwicklung. Um Missbrauch zu vermeiden, musst du {remaining}s warten.",
    "invalid_link": "Bitte sende einen gültigen Terabox-Link.",
    "sending_media": "Sende dir die Medien...🤤",
    "download_failed": (
        "Download fehlgeschlagen ❌\n\n"
        "Grund: Der Link ist möglicherweise defekt oder es ist ein "
        "Ordner-Link.\nNur Datei-Links werden unterstützt."
    ),
    "file_deleted_warning": "⚠️ Diese Datei wird in 10 Minuten automatisch gelöscht. Leite sie weiter, um sie zu behalten.",
    "no_videos": "Noch keine Videos indexiert. Der Besitzer kann /refresh verwenden, um den Index zu erstellen.",
    "mongo_missing": "MongoDB ist nicht konfiguriert.",
    "search_usage": "Verwendung: /search <1 bis 3 Stichwörter>",
    "search_no_results": "Keine Datei gefunden, die allen angegebenen Stichwörtern entspricht.",
    "search_unavailable": "Die Suche ist vorübergehend nicht verfügbar. Bitte versuche es erneut.",
    "search_expired": "Diese Suche ist abgelaufen. Sende /search erneut.",
    "search_not_yours": "Diese Suche gehört einem anderen Benutzer.",
    "search_none_left": "Es sind keine passenden Dateien mehr verfügbar.",
    "search_send_failed": "Diese Datei konnte nicht gesendet werden. Sie wurde möglicherweise aus dem Quellkanal entfernt.",
    "search_header": "🔎 Suche: {keywords}\n{count} passende Dateien gefunden. Wähle unten einen Dateinamen aus.",
    "search_sending": "Datei wird gesendet...",
    "search_file_unavailable": "Diese Datei ist nicht mehr verfügbar.",
    "dump_caption": (
        "💾 Permanenter Dump-Kanal-Zugang\n\n"
        "Kaufe permanenten Zugang zum gesamten Dump-Kanal.\n\n"
        "• Binance: nur 1,5 USDT\n"
        "• UPI: nur 200 ₹\n\n"
        "Wähle unten deine Zahlungsmethode. Sende nach der Zahlung den "
        "Zahlungs-Screenshot zur Überprüfung an @rtx5069."
    ),
    "dump_qr_binance": (
        "Binance-Zahlung\n\n"
        "Betrag: nur 1,5 USDT\n\n"
        "Scanne diesen QR mit der Binance-App. Sende nach der Zahlung den "
        "Screenshot zur Überprüfung an @rtx5069."
    ),
    "dump_qr_upi": (
        "UPI-Zahlung\n\n"
        "Betrag: nur 200 ₹\n\n"
        "Scanne diesen QR mit einer beliebigen UPI-App. Sende nach der "
        "Zahlung den Screenshot zur Überprüfung an @rtx5069."
    ),
    "dump_qr_error": "Zahlungs-QR konnte nicht angezeigt werden. Sende /dump und versuche es erneut.",
    "dump_unavailable": "Dump-Zugangsinformationen sind vorübergehend nicht verfügbar.",
    "dump_menu_unavailable": "Zahlungsmenü ist vorübergehend nicht verfügbar.",
    "select_language": "🌐 Wähle deine Sprache:",
    "language_saved": "✅ Sprache festgelegt: {language}",
    "confirm": "✅ Bestätigen",
    "settings_title": "⚙️ Benutzereinstellungen",
}




