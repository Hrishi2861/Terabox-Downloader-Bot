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
        "• Binance: 2.75 USDT only\n"
        "• UPI: ₹250 only\n\n"
        "Choose your payment method below. After paying, send the payment "
        "screenshot to @rtx5069 for verification."
    ),
    "dump_qr_binance": (
        "Binance Payment\n\n"
        "Amount: 2.75 USDT only\n\n"
        "Scan this QR using the Binance app. After paying, send the "
        "payment screenshot to @rtx5069 for verification."
    ),
    "dump_qr_upi": (
        "UPI Payment\n\n"
        "Amount: ₹250 only\n\n"
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
        "• Binance: केवल 2.75 USDT\n"
        "• UPI: केवल ₹250\n\n"
        "नीचे अपनी भुगतान विधि चुनें। भुगतान के बाद, सत्यापन के लिए भुगतान "
        "स्क्रीनशॉट @rtx5069 को भेजें।"
    ),
    "dump_qr_binance": (
        "Binance भुगतान\n\n"
        "राशि: केवल 2.75 USDT\n\n"
        "Binance ऐप से यह QR स्कैन करें। भुगतान के बाद, सत्यापन के लिए भुगतान "
        "स्क्रीनशॉट @rtx5069 को भेजें।"
    ),
    "dump_qr_upi": (
        "UPI भुगतान\n\n"
        "राशि: केवल ₹250\n\n"
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
        "• Binance: फक्त 2.75 USDT\n"
        "• UPI: फक्त ₹250\n\n"
        "खाली तुमची पेमेंट पद्धत निवडा. पेमेंटनंतर, पडताळणीसाठी पेमेंट "
        "स्क्रीनशॉट @rtx5069 यांना पाठवा."
    ),
    "dump_qr_binance": (
        "Binance पेमेंट\n\n"
        "रक्कम: फक्त 2.75 USDT\n\n"
        "Binance अॅपने हा QR स्कॅन करा. पेमेंटनंतर, पडताळणीसाठी पेमेंट "
        "स्क्रीनशॉट @rtx5069 यांना पाठवा."
    ),
    "dump_qr_upi": (
        "UPI पेमेंट\n\n"
        "रक्कम: फक्त ₹250\n\n"
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
        "• Binance: মাত্র 2.75 USDT\n"
        "• UPI: মাত্র ₹250\n\n"
        "নিচে আপনার পেমেন্ট পদ্ধতি নির্বাচন করুন। পেমেন্টের পরে, যাচাইয়ের "
        "জন্য পেমেন্ট স্ক্রিনশট @rtx5069 কে পাঠান।"
    ),
    "dump_qr_binance": (
        "Binance পেমেন্ট\n\n"
        "পরিমাণ: মাত্র 2.75 USDT\n\n"
        "Binance অ্যাপ দিয়ে এই QR স্ক্যান করুন। পেমেন্টের পরে, যাচাইয়ের "
        "জন্য পেমেন্ট স্ক্রিনশট @rtx5069 কে পাঠান।"
    ),
    "dump_qr_upi": (
        "UPI পেমেন্ট\n\n"
        "পরিমাণ: মাত্র ₹250\n\n"
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
        "• Binance: 2.75 USDT மட்டும்\n"
        "• UPI: ₹250 மட்டும்\n\n"
        "கீழே உங்கள் பணம் செலுத்தும் முறையைத் தேர்ந்தெடுங்கள். பணம் "
        "செலுத்திய பிறகு, சரிபார்ப்புக்கு திரைப்படத்தை @rtx5069 க்கு அனுப்பவும்."
    ),
    "dump_qr_binance": (
        "Binance பணப்பரிமாற்றம்\n\n"
        "தொகை: 2.75 USDT மட்டும்\n\n"
        "Binance ஆப்பின் மூலம் இந்த QR ஐ ஸ்கேன் செய்யுங்கள். பணம் "
        "செலுத்திய பிறகு, சரிபார்ப்புக்கு ஸ்கிரீன்ஷாட்டை @rtx5069 க்கு அனுப்பவும்."
    ),
    "dump_qr_upi": (
        "UPI பணப்பரிமாற்றம்\n\n"
        "தொகை: ₹250 மட்டும்\n\n"
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
        "• Binance: 2.75 USDT మాత్రమే\n"
        "• UPI: ₹250 మాత్రమే\n\n"
        "దిగువ మీ చెల్లింపు విధానాన్ని ఎంచుకోండి. చెల్లింపు తర్వాత, "
        "ధృవీకరణ కోసం స్క్రీన్‌షాట్‌ను @rtx5069 కు పంపండి."
    ),
    "dump_qr_binance": (
        "Binance చెల్లింపు\n\n"
        "మొత్తం: 2.75 USDT మాత్రమే\n\n"
        "Binance యాప్‌తో ఈ QR ను స్కాన్ చేయండి. చెల్లింపు తర్వాత, "
        "ధృవీకరణ కోసం స్క్రీన్‌షాట్‌ను @rtx5069 కు పంపండి."
    ),
    "dump_qr_upi": (
        "UPI చెల్లింపు\n\n"
        "మొత్తం: ₹250 మాత్రమే\n\n"
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
        "• Binance: 2.75 USDT ಮಾತ್ರ\n"
        "• UPI: ₹250 ಮಾತ್ರ\n\n"
        "ಕೆಳಗೆ ನಿಮ್ಮ ಪಾವತಿ ವಿಧಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ. ಪಾವತಿಸಿದ ನಂತರ, "
        "ಪರಿಶೀಲನೆಗಾಗಿ ಪಾವತಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು @rtx5069 ಗೆ ಕಳುಹಿಸಿ."
    ),
    "dump_qr_binance": (
        "Binance ಪಾವತಿ\n\n"
        "ಮೊತ್ತ: 2.75 USDT ಮಾತ್ರ\n\n"
        "Binance ಆಪ್‌ನಿಂದ ಈ QR ಅನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ. ಪಾವತಿಸಿದ ನಂತರ, "
        "ಪರಿಶೀಲನೆಗಾಗಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು @rtx5069 ಗೆ ಕಳುಹಿಸಿ."
    ),
    "dump_qr_upi": (
        "UPI ಪಾವತಿ\n\n"
        "ಮೊತ್ತ: ₹250 ಮಾತ್ರ\n\n"
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
        "• Binance: 2.75 USDT മാത്രം\n"
        "• UPI: ₹250 മാത്രം\n\n"
        "താഴെ നിങ്ങളുടെ പണമടയ്ക്കൽ രീതി തിരഞ്ഞെടുക്കുക. പണമടച്ച ശേഷം, "
        "സ്ഥിരീകരണത്തിനായി സ്ക്രീൻഷോട്ട് @rtx5069 ന് അയയ്ക്കുക."
    ),
    "dump_qr_binance": (
        "Binance പണമടയ്ക്കൽ\n\n"
        "തുക: 2.75 USDT മാത്രം\n\n"
        "Binance ആപ്പ് ഉപയോഗിച്ച് ഈ QR സ്കാൻ ചെയ്യുക. പണമടച്ച ശേഷം, "
        "സ്ഥിരീകരണത്തിനായി സ്ക്രീൻഷോട്ട് @rtx5069 ന് അയയ്ക്കുക."
    ),
    "dump_qr_upi": (
        "UPI പണമടയ്ക്കൽ\n\n"
        "തുക: ₹250 മാത്രം\n\n"
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
        "• Binance: صرف 2.75 USDT\n"
        "• UPI: صرف ₹250\n\n"
        "نیچے اپنی ادائیگی کا طریقہ منتخب کریں۔ ادائیگی کے بعد، تصدیق کے "
        "لیے ادائیگی کا اسکرین شاٹ @rtx5069 کو بھیجیں۔"
    ),
    "dump_qr_binance": (
        "Binance ادائیگی\n\n"
        "رقم: صرف 2.75 USDT\n\n"
        "Binance ایپ سے یہ QR سکین کریں۔ ادائیگی کے بعد، تصدیق کے لیے "
        "اسکرین شاٹ @rtx5069 کو بھیجیں۔"
    ),
    "dump_qr_upi": (
        "UPI ادائیگی\n\n"
        "رقم: صرف ₹250\n\n"
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
        "• Binance: ਸਿਰਫ਼ 2.75 USDT\n"
        "• UPI: ਸਿਰਫ਼ ₹250\n\n"
        "ਹੇਠਾਂ ਆਪਣਾ ਭੁਗਤਾਨ ਤਰੀਕਾ ਚੁਣੋ। ਭੁਗਤਾਨ ਤੋਂ ਬਾਅਦ, ਤਸਦੀਕ ਲਈ "
        "ਭੁਗਤਾਨ ਸਕਰੀਨਸ਼ਾਟ @rtx5069 ਨੂੰ ਭੇਜੋ।"
    ),
    "dump_qr_binance": (
        "Binance ਭੁਗਤਾਨ\n\n"
        "ਰਕਮ: ਸਿਰਫ਼ 2.75 USDT\n\n"
        "Binance ਐਪ ਨਾਲ ਇਹ QR ਸਕੈਨ ਕਰੋ। ਭੁਗਤਾਨ ਤੋਂ ਬਾਅਦ, ਤਸਦੀਕ ਲਈ "
        "ਸਕਰੀਨਸ਼ਾਟ @rtx5069 ਨੂੰ ਭੇਜੋ।"
    ),
    "dump_qr_upi": (
        "UPI ਭੁਗਤਾਨ\n\n"
        "ਰਕਮ: ਸਿਰਫ਼ ₹250\n\n"
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
        "• Binance: ફક્ત 2.75 USDT\n"
        "• UPI: ફક્ત ₹250\n\n"
        "નીચે તમારી ચુકવણી પદ્ધતિ પસંદ કરો. ચુકવણી પછી, ચકાસણી માટે "
        "ચુકવણી સ્ક્રીનશોટ @rtx5069 ને મોકલો."
    ),
    "dump_qr_binance": (
        "Binance ચુકવણી\n\n"
        "રકમ: ફક્ત 2.75 USDT\n\n"
        "Binance એપથી આ QR સ્કેન કરો. ચુકવણી પછી, ચકાસણી માટે "
        "સ્ક્રીનશોટ @rtx5069 ને મોકલો."
    ),
    "dump_qr_upi": (
        "UPI ચુકવણી\n\n"
        "રકમ: ફક્ત ₹250\n\n"
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
        "• Binance: solo 2.75 USDT\n"
        "• UPI: solo ₹250\n\n"
        "Elige tu método de pago abajo. Tras pagar, envía la captura del "
        "pago a @rtx5069 para verificarlo."
    ),
    "dump_qr_binance": (
        "Pago con Binance\n\n"
        "Importe: solo 2.75 USDT\n\n"
        "Escanea este código QR con la app de Binance. Tras pagar, envía "
        "la captura a @rtx5069 para verificarlo."
    ),
    "dump_qr_upi": (
        "Pago por UPI\n\n"
        "Importe: solo ₹250\n\n"
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
        "• Binance : seulement 2,75 USDT\n"
        "• UPI : seulement 250 ₹\n\n"
        "Choisissez votre moyen de paiement ci-dessous. Après paiement, "
        "envoyez la capture d'écran à @rtx5069 pour vérification."
    ),
    "dump_qr_binance": (
        "Paiement Binance\n\n"
        "Montant : seulement 2,75 USDT\n\n"
        "Scannez ce QR avec l'application Binance. Après paiement, envoyez "
        "la capture d'écran à @rtx5069 pour vérification."
    ),
    "dump_qr_upi": (
        "Paiement UPI\n\n"
        "Montant : seulement 250 ₹\n\n"
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
        "• Binance: nur 2,75 USDT\n"
        "• UPI: nur 250 ₹\n\n"
        "Wähle unten deine Zahlungsmethode. Sende nach der Zahlung den "
        "Zahlungs-Screenshot zur Überprüfung an @rtx5069."
    ),
    "dump_qr_binance": (
        "Binance-Zahlung\n\n"
        "Betrag: nur 2,75 USDT\n\n"
        "Scanne diesen QR mit der Binance-App. Sende nach der Zahlung den "
        "Screenshot zur Überprüfung an @rtx5069."
    ),
    "dump_qr_upi": (
        "UPI-Zahlung\n\n"
        "Betrag: nur 250 ₹\n\n"
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

# Extended keys for thumbnail and leech destination settings.
EXTRA_TRANSLATIONS = {}

EXTRA_TRANSLATIONS["en"] = {
    "settings_status": "⚙️ User Settings\n\nLanguage: {language}\nThumbnail: {thumb}\nDestination: {dest}",
    "dest_default": "Default (this chat)",
    "thumb_set_prompt": "🖼️ Send me a photo now to set it as your custom thumbnail.",
    "thumb_invalid": "❌ Could not process that image. Please try another photo.",
    "thumb_set_done": "✅ Custom thumbnail set.",
    "thumb_removed": "✅ Custom thumbnail removed.",
    "dest_set_prompt": "📥 Send me your channel/group ID now (e.g. -1001234567890).",
    "dest_set_done": "✅ Leech destination set: {title}",
    "dest_removed": "✅ Leech destination removed. Videos will be sent to this chat.",
    "dest_invalid": "❌ Invalid channel/group ID. It should look like -1001234567890. Send /user_settings to try again.",
    "dest_no_access": "❌ I need to be an admin in that chat first. Add me there as admin and try again.",
    "dest_not_admin": "❌ You must be an admin of that chat to set it as your destination.",
    "dest_send_failed": "⚠️ Could not send to your destination, so I sent it here instead.",
    "dest_delivered": "✅ Video delivered to your destination: {title}",
    "cancel_pending": "❌ Pending setting cancelled.",
}

EXTRA_TRANSLATIONS["hi"] = {
    "settings_status": "⚙️ उपयोगकर्ता सेटिंग्स\n\nभाषा: {language}\nथंबनेल: {thumb}\nगंतव्य: {dest}",
    "dest_default": "डिफ़ॉल्ट (यह चैट)",
    "thumb_set_prompt": "🖼️ कस्टम थंबनेल सेट करने के लिए अब मुझे एक फोटो भेजें।",
    "thumb_invalid": "❌ वह इमेज प्रोसेस नहीं हो सकी। कृपया कोई अन्य फोटो भेजें।",
    "thumb_set_done": "✅ कस्टम थंबनेल सेट हो गया।",
    "thumb_removed": "✅ कस्टम थंबनेल हटा दिया गया।",
    "dest_set_prompt": "📥 अब अपना चैनल/ग्रुप आईडी भेजें (जैसे -1001234567890)।",
    "dest_set_done": "✅ लीच गंतव्य सेट: {title}",
    "dest_removed": "✅ लीच गंतव्य हटा दिया गया। वीडियो अब इस चैट में भेजे जाएँगे।",
    "dest_invalid": "❌ अमान्य चैनल/ग्रुप आईडी। यह -1001234567890 जैसी होनी चाहिए। फिर से कोशिश के लिए /user_settings भेजें।",
    "dest_no_access": "❌ पहले मुझे उस चैट में एडमिन बनाएँ। मुझे वहाँ एडमिन जोड़ें और फिर से कोशिश करें।",
    "dest_not_admin": "❌ उस चैट को गंतव्य बनाने के लिए आपको उसके एडमिन होना चाहिए।",
    "dest_send_failed": "⚠️ आपके गंतव्य पर नहीं भेजा जा सका, इसलिए यहाँ भेज दिया।",
    "dest_delivered": "✅ वीडियो आपके गंतव्य पर भेज दिया: {title}",
    "cancel_pending": "❌ लंबित सेटिंग रद्द कर दी गई।",
}

EXTRA_TRANSLATIONS["mr"] = {
    "settings_status": "⚙️ वापरकर्ता सेटिंग्ज\n\nभाषा: {language}\nथंबनेल: {thumb}\nगंतव्य: {dest}",
    "dest_default": "डीफॉल्ट (ही चॅट)",
    "thumb_set_prompt": "🖼️ सानुकूल थंबनेल सेट करण्यासाठी आता मला फोटो पाठवा.",
    "thumb_invalid": "❌ ती प्रतिमा प्रक्रिया करता आली नाही. कृपया दुसरा फोटो पाठवा.",
    "thumb_set_done": "✅ सानुकूल थंबनेल सेट झाले.",
    "thumb_removed": "✅ सानुकूल थंबनेल काढले.",
    "dest_set_prompt": "📥 आता तुमचा चॅनेल/ग्रुप आयडी पाठवा (उदा. -1001234567890).",
    "dest_set_done": "✅ लीच गंतव्य सेट: {title}",
    "dest_removed": "✅ लीच गंतव्य काढले. व्हिडिओ आता या चॅटमध्ये पाठवले जातील.",
    "dest_invalid": "❌ अवैध चॅनेल/ग्रुप आयडी. तो -1001234567890 सारखा असावा. पुन्हा प्रयत्न करण्यासाठी /user_settings पाठवा.",
    "dest_no_access": "❌ प्रथम त्या चॅटमध्ये मला ॲडमिन करा. मला ॲडमिन म्हणून जोडा आणि पुन्हा प्रयत्न करा.",
    "dest_not_admin": "❌ ते गंतव्य ठेवण्यासाठी तुम्ही त्या चॅटचे ॲडमिन असले पाहिजे.",
    "dest_send_failed": "⚠️ तुमच्या गंतव्यास पाठवता आले नाही, म्हणून येथे पाठवले.",
    "dest_delivered": "✅ व्हिडिओ तुमच्या गंतव्यास पाठवला: {title}",
    "cancel_pending": "❌ प्रलंबित सेटिंग रद्द केली.",
}

EXTRA_TRANSLATIONS["bn"] = {
    "settings_status": "⚙️ ব্যবহারকারীর সেটিংস\n\nভাষা: {language}\nথাম্বনেইল: {thumb}\nগন্তব্য: {dest}",
    "dest_default": "ডিফল্ট (এই চ্যাট)",
    "thumb_set_prompt": "🖼️ কাস্টম থাম্বনেইল সেট করতে এখন আমাকে একটি ছবি পাঠান।",
    "thumb_invalid": "❌ ছবিটি প্রসেস করা যায়নি। অনুগ্রহ করে অন্য একটি ছবি পাঠান।",
    "thumb_set_done": "✅ কাস্টম থাম্বনেইল সেট হয়েছে।",
    "thumb_removed": "✅ কাস্টম থাম্বনেইল সরানো হয়েছে।",
    "dest_set_prompt": "📥 এখন আপনার চ্যানেল/গ্রুপ আইডি পাঠান (যেমন -1001234567890)।",
    "dest_set_done": "✅ লিচ গন্তব্য সেট: {title}",
    "dest_removed": "✅ লিচ গন্তব্য সরানো হয়েছে। ভিডিও এখন এই চ্যাটে পাঠানো হবে।",
    "dest_invalid": "❌ অবৈধ চ্যানেল/গ্রুপ আইডি। এটি -1001234567890 এর মতো হওয়া উচিত। আবার চেষ্টা করতে /user_settings পাঠান।",
    "dest_no_access": "❌ প্রথমে আমাকে সেই চ্যাটে অ্যাডমিন করুন। আমাকে অ্যাডমিন করে আবার চেষ্টা করুন।",
    "dest_not_admin": "❌ গন্তব্য হিসেবে সেট করতে আপনাকে সেই চ্যাটের অ্যাডমিন হতে হবে।",
    "dest_send_failed": "⚠️ আপনার গন্তব্যে পাঠানো যায়নি, তাই এখানে পাঠানো হলো।",
    "dest_delivered": "✅ ভিডিও আপনার গন্তব্যে পাঠানো হয়েছে: {title}",
    "cancel_pending": "❌ অপেক্ষমাণ সেটিং বাতিল করা হয়েছে।",
}

EXTRA_TRANSLATIONS["ta"] = {
    "settings_status": "⚙️ பயனர் அமைப்புகள்\n\nமொழி: {language}\nசிறுபடம்: {thumb}\nஇலக்கு: {dest}",
    "dest_default": "இயல்புநிலை (இந்த அரட்டை)",
    "thumb_set_prompt": "🖼️ தனிப்பயன் சிறுபடமாக அமைக்க இப்போது எனக்கு ஒரு படத்தை அனுப்புங்கள்.",
    "thumb_invalid": "❌ அந்த படத்தை செயலாக்க முடியவில்லை. வேறு படம் அனுப்புங்கள்.",
    "thumb_set_done": "✅ தனிப்பயன் சிறுபடம் அமைக்கப்பட்டது.",
    "thumb_removed": "✅ தனிப்பயன் சிறுபடம் நீக்கப்பட்டது.",
    "dest_set_prompt": "📥 இப்போது உங்கள் சேனல்/குழு ஐடியை அனுப்புங்கள் (எ.கா. -1001234567890).",
    "dest_set_done": "✅ இலக்கு அமைக்கப்பட்டது: {title}",
    "dest_removed": "✅ இலக்கு நீக்கப்பட்டது. வீடியோக்கள் இனி இந்த அரட்டைக்கு அனுப்பப்படும்.",
    "dest_invalid": "❌ தவறான சேனல்/குழு ஐடி. அது -1001234567890 போல இருக்க வேண்டும். மீண்டும் முயற்சிக்க /user_settings அனுப்புங்கள்.",
    "dest_no_access": "❌ முதலில் அந்த அரட்டையில் என்னை நிர்வாகியாக ஆக்குங்கள். என்னை நிர்வாகியாகச் சேர்த்து மீண்டும் முயற்சிக்கவும்.",
    "dest_not_admin": "❌ இலக்காக அமைக்க நீங்கள் அந்த அரட்டையின் நிர்வாகியாக இருக்க வேண்டும்.",
    "dest_send_failed": "⚠️ உங்கள் இலக்குக்கு அனுப்ப முடியவில்லை, எனவே இங்கே அனுப்பினேன்.",
    "dest_delivered": "✅ வீடியோ உங்கள் இலக்குக்கு அனுப்பப்பட்டது: {title}",
    "cancel_pending": "❌ நிலுவையில் உள்ள அமைப்பு ரத்து செய்யப்பட்டது.",
}

EXTRA_TRANSLATIONS["te"] = {
    "settings_status": "⚙️ యూజర్ సెట్టింగ్‌లు\n\nభాష: {language}\nథంబ్‌నెయిల్: {thumb}\nగమ్యం: {dest}",
    "dest_default": "డిఫాల్ట్ (ఈ చాట్)",
    "thumb_set_prompt": "🖼️ కస్టమ్ థంబ్‌నెయిల్‌గా సెట్ చేయడానికి ఇప్పుడు నాకు ఒక ఫోటో పంపండి.",
    "thumb_invalid": "❌ ఆ చిత్రాన్ని ప్రాసెస్ చేయడం సాధ్యం కాలేదు. దయచేసి మరో ఫోటో పంపండి.",
    "thumb_set_done": "✅ కస్టమ్ థంబ్‌నెయిల్ సెట్ చేయబడింది.",
    "thumb_removed": "✅ కస్టమ్ థంబ్‌నెయిల్ తీసివేయబడింది.",
    "dest_set_prompt": "📥 ఇప్పుడు మీ ఛానల్/గ్రూప్ ఐడీ పంపండి (ఉదా. -1001234567890).",
    "dest_set_done": "✅ లీచ్ గమ్యం సెట్ చేయబడింది: {title}",
    "dest_removed": "✅ లీచ్ గమ్యం తీసివేయబడింది. వీడియోలు ఇప్పుడు ఈ చాట్‌కు పంపబడతాయి.",
    "dest_invalid": "❌ తప్పు ఛానల్/గ్రూప్ ఐడీ. అది -1001234567890 లాగా ఉండాలి. మళ్లీ ప్రయత్నించడానికి /user_settings పంపండి.",
    "dest_no_access": "❌ ముందుగా ఆ చాట్‌లో నన్ను అడ్మిన్‌గా చేయండి. నన్ను అడ్మిన్‌గా జోడించి మళ్లీ ప్రయత్నించండి.",
    "dest_not_admin": "❌ గమ్యంగా సెట్ చేయడానికి మీరు ఆ చాట్‌కు అడ్మిన్ కావాలి.",
    "dest_send_failed": "⚠️ మీ గమ్యానికి పంపలేకపోయాను, కాబట్టి ఇక్కడికి పంపాను.",
    "dest_delivered": "✅ వీడియో మీ గమ్యానికి పంపబడింది: {title}",
    "cancel_pending": "❌ పెండింగ్ సెట్టింగ్ రద్దు చేయబడింది.",
}

EXTRA_TRANSLATIONS["kn"] = {
    "settings_status": "⚙️ ಬಳಕೆದಾರರ ಸೆಟ್ಟಿಂಗ್‌ಗಳು\n\nಭಾಷೆ: {language}\nಥಂಬ್‌ನೇಲ್: {thumb}\nಗುರಿ: {dest}",
    "dest_default": "ಡೀಫಾಲ್ಟ್ (ಈ ಚಾಟ್)",
    "thumb_set_prompt": "🖼️ ಕಸ್ಟಮ್ ಥಂಬ್‌ನೇಲ್ ಆಗಿ ಹೊಂದಿಸಲು ಈಗ ನನಗೆ ಒಂದು ಫೋಟೋ ಕಳುಹಿಸಿ.",
    "thumb_invalid": "❌ ಆ ಚಿತ್ರವನ್ನು ಪ್ರೋಸೆಸ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಬೇರೊಂದು ಫೋಟೋ ಕಳುಹಿಸಿ.",
    "thumb_set_done": "✅ ಕಸ್ಟಮ್ ಥಂಬ್‌ನೇಲ್ ಹೊಂದಿಸಲಾಗಿದೆ.",
    "thumb_removed": "✅ ಕಸ್ಟಮ್ ಥಂಬ್‌ನೇಲ್ ತೆಗೆದುಹಾಕಲಾಗಿದೆ.",
    "dest_set_prompt": "📥 ಈಗ ನಿಮ್ಮ ಚಾನೆಲ್/ಗ್ರೂಪ್ ಐಡಿ ಕಳುಹಿಸಿ (ಉದಾ. -1001234567890).",
    "dest_set_done": "✅ ಲೀಚ್ ಗುರಿ ಹೊಂದಿಸಲಾಗಿದೆ: {title}",
    "dest_removed": "✅ ಲೀಚ್ ಗುರಿ ತೆಗೆದುಹಾಕಲಾಗಿದೆ. ವೀಡಿಯೊಗಳು ಈಗ ಈ ಚಾಟ್‌ಗೆ ಕಳುಹಿಸಲ್ಪಡುತ್ತವೆ.",
    "dest_invalid": "❌ ಅಮಾನ್ಯ ಚಾನೆಲ್/ಗ್ರೂಪ್ ಐಡಿ. ಅದು -1001234567890 ನಂತೆ ಇರಬೇಕು. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಲು /user_settings ಕಳುಹಿಸಿ.",
    "dest_no_access": "❌ ಮೊದಲು ಆ ಚಾಟ್‌ನಲ್ಲಿ ನನ್ನನ್ನು ಅಡ್ಮಿನ್ ಮಾಡಿ. ನನ್ನನ್ನು ಅಡ್ಮಿನ್ ಆಗಿ ಸೇರಿಸಿ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    "dest_not_admin": "❌ ಗುರಿಯಾಗಿ ಹೊಂದಿಸಲು ನೀವು ಆ ಚಾಟ್‌ನ ಅಡ್ಮಿನ್ ಆಗಿರಬೇಕು.",
    "dest_send_failed": "⚠️ ನಿಮ್ಮ ಗುರಿಗೆ ಕಳುಹಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ, ಆದ್ದರಿಂದ ಇಲ್ಲಿ ಕಳುಹಿಸಿದೆ.",
    "dest_delivered": "✅ ವೀಡಿಯೊ ನಿಮ್ಮ ಗುರಿಗೆ ಕಳುಹಿಸಲಾಗಿದೆ: {title}",
    "cancel_pending": "❌ ಬಾಕಿ ಇರುವ ಸೆಟ್ಟಿಂಗ್ ರದ್ದುಪಡಿಸಲಾಗಿದೆ.",
}

EXTRA_TRANSLATIONS["ml"] = {
    "settings_status": "⚙️ ഉപയോക്തൃ ക്രമീകരണങ്ങൾ\n\nഭാഷ: {language}\nതംബ്നെയിൽ: {thumb}\nലക്ഷ്യം: {dest}",
    "dest_default": "സ്ഥിരസ്ഥിതി (ഈ ചാറ്റ്)",
    "thumb_set_prompt": "🖼️ ഇഷ്ടാനുസൃത തംബ്നെയിൽ ആയി സജ്ജമാക്കാൻ ഇപ്പോൾ എനിക്ക് ഒരു ഫോട്ടോ അയയ്ക്കുക.",
    "thumb_invalid": "❌ ആ ചിത്രം പ്രോസസ്സ് ചെയ്യാൻ കഴിഞ്ഞില്ല. ദയവായി മറ്റൊരു ഫോട്ടോ അയയ്ക്കുക.",
    "thumb_set_done": "✅ ഇഷ്ടാനുസൃത തംബ്നെയിൽ സജ്ജമാക്കി.",
    "thumb_removed": "✅ ഇഷ്ടാനുസൃത തംബ്നെയിൽ നീക്കം ചെയ്തു.",
    "dest_set_prompt": "📥 ഇപ്പോൾ നിങ്ങളുടെ ചാനൽ/ഗ്രൂപ്പ് ഐഡി അയയ്ക്കുക (ഉദാ. -1001234567890).",
    "dest_set_done": "✅ ലീച്ച് ലക്ഷ്യം സജ്ജമാക്കി: {title}",
    "dest_removed": "✅ ലീച്ച് ലക്ഷ്യം നീക്കം ചെയ്തു. വീഡിയോകൾ ഇനി ഈ ചാറ്റിലേക്ക് അയയ്ക്കും.",
    "dest_invalid": "❌ അസാധുവായ ചാനൽ/ഗ്രൂപ്പ് ഐഡി. അത് -1001234567890 പോലെ ആയിരിക്കണം. വീണ്ടും ശ്രമിക്കാൻ /user_settings അയയ്ക്കുക.",
    "dest_no_access": "❌ ആദ്യം ആ ചാറ്റിൽ എന്നെ അഡ്മിൻ ആക്കുക. എന്നെ അഡ്മിനായി ചേർത്ത് വീണ്ടും ശ്രമിക്കുക.",
    "dest_not_admin": "❌ ലക്ഷ്യമായി സജ്ജമാക്കാൻ നിങ്ങൾ ആ ചാറ്റിന്റെ അഡ്മിൻ ആയിരിക്കണം.",
    "dest_send_failed": "⚠️ നിങ്ങളുടെ ലക്ഷ്യത്തിലേക്ക് അയയ്ക്കാൻ കഴിഞ്ഞില്ല, അതിനാൽ ഇവിടെ അയച്ചു.",
    "dest_delivered": "✅ വീഡിയോ നിങ്ങളുടെ ലക്ഷ്യത്തിലേക്ക് അയച്ചു: {title}",
    "cancel_pending": "❌ താൽക്കാലിക ക്രമീകരണം റദ്ദാക്കി.",
}

EXTRA_TRANSLATIONS["ur"] = {
    "settings_status": "⚙️ صارف سیٹنگز\n\nزبان: {language}\nتھمب نیل: {thumb}\nمنزل: {dest}",
    "dest_default": "ڈیفالٹ (یہ چیٹ)",
    "thumb_set_prompt": "🖼️ اپنی مرضی کا تھمب نیل مقرر کرنے کے لیے اب مجھے ایک تصویر بھیجیں۔",
    "thumb_invalid": "❌ وہ تصویر پروسیس نہیں ہو سکی۔ براہ کرم کوئی اور تصویر بھیجیں۔",
    "thumb_set_done": "✅ اپنی مرضی کا تھمب نیل مقرر ہو گیا۔",
    "thumb_removed": "✅ اپنی مرضی کا تھمب نیل ہٹا دیا گیا۔",
    "dest_set_prompt": "📥 اب اپنا چینل/گروپ آئی ڈی بھیجیں (مثلاً -1001234567890)۔",
    "dest_set_done": "✅ لیز منزل مقرر: {title}",
    "dest_removed": "✅ لیز منزل ہٹا دی گئی۔ ویڈیوز اب اسی چیٹ میں بھیجی جائیں گی۔",
    "dest_invalid": "❌ غلط چینل/گروپ آئی ڈی۔ یہ -1001234567890 جیسی ہونی چاہیے۔ دوبارہ کوشش کے لیے /user_settings بھیجیں۔",
    "dest_no_access": "❌ پہلے مجھے اس چیٹ میں ایڈمن بنائیں۔ مجھے ایڈمن کے طور پر شامل کریں اور دوبارہ کوشش کریں۔",
    "dest_not_admin": "❌ منزل مقرر کرنے کے لیے آپ کا اس چیٹ کا ایڈمن ہونا ضروری ہے۔",
    "dest_send_failed": "⚠️ آپ کی منزل تک نہیں بھیجی جا سکی، اس لیے یہاں بھیج دیا۔",
    "dest_delivered": "✅ ویڈیو آپ کی منزل پر بھیج دی گئی: {title}",
    "cancel_pending": "❌ زیر التوا سیٹنگ منسوخ کر دی گئی۔",
}

EXTRA_TRANSLATIONS["pa"] = {
    "settings_status": "⚙️ ਵਰਤੋਂਕਾਰ ਸੈਟਿੰਗਾਂ\n\nਭਾਸ਼ਾ: {language}\nਥੰਮਨੇਲ: {thumb}\nਮੰਜ਼ਿਲ: {dest}",
    "dest_default": "ਮੂਲ (ਇਹ ਚੈਟ)",
    "thumb_set_prompt": "🖼️ ਕਸਟਮ ਥੰਮਨੇਲ ਸੈੱਟ ਕਰਨ ਲਈ ਹੁਣ ਮੈਨੂੰ ਇੱਕ ਫੋਟੋ ਭੇਜੋ।",
    "thumb_invalid": "❌ ਉਹ ਤਸਵੀਰ ਪ੍ਰੋਸੈਸ ਨਹੀਂ ਹੋ ਸਕੀ। ਕਿਰਪਾ ਕਰਕੇ ਹੋਰ ਫੋਟੋ ਭੇਜੋ।",
    "thumb_set_done": "✅ ਕਸਟਮ ਥੰਮਨੇਲ ਸੈੱਟ ਹੋ ਗਿਆ।",
    "thumb_removed": "✅ ਕਸਟਮ ਥੰਮਨੇਲ ਹਟਾ ਦਿੱਤਾ ਗਿਆ।",
    "dest_set_prompt": "📥 ਹੁਣ ਆਪਣੀ ਚੈਨਲ/ਗਰੁੱਪ ਆਈਡੀ ਭੇਜੋ (ਜਿਵੇਂ -1001234567890)।",
    "dest_set_done": "✅ ਲੀਚ ਮੰਜ਼ਿਲ ਸੈੱਟ: {title}",
    "dest_removed": "✅ ਲੀਚ ਮੰਜ਼ਿਲ ਹਟਾ ਦਿੱਤੀ ਗਈ। ਵੀਡੀਓ ਹੁਣ ਇਸ ਚੈਟ ਵਿੱਚ ਭੇਜੇ ਜਾਣਗੇ।",
    "dest_invalid": "❌ ਗਲਤ ਚੈਨਲ/ਗਰੁੱਪ ਆਈਡੀ। ਇਹ -1001234567890 ਵਰਗੀ ਹੋਣੀ ਚਾਹੀਦੀ ਹੈ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਲਈ /user_settings ਭੇਜੋ।",
    "dest_no_access": "❌ ਪਹਿਲਾਂ ਮੈਨੂੰ ਉਸ ਚੈਟ ਵਿੱਚ ਐਡਮਿਨ ਬਣਾਓ। ਮੈਨੂੰ ਐਡਮਿਨ ਵਜੋਂ ਜੋੜੋ ਅਤੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
    "dest_not_admin": "❌ ਮੰਜ਼ਿਲ ਸੈੱਟ ਕਰਨ ਲਈ ਤੁਹਾਨੂੰ ਉਸ ਚੈਟ ਦਾ ਐਡਮਿਨ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ।",
    "dest_send_failed": "⚠️ ਤੁਹਾਡੀ ਮੰਜ਼ਿਲ 'ਤੇ ਨਹੀਂ ਭੇਜਿਆ ਜਾ ਸਕਿਆ, ਇਸ ਲਈ ਇੱਥੇ ਭੇਜ ਦਿੱਤਾ।",
    "dest_delivered": "✅ ਵੀਡੀਓ ਤੁਹਾਡੀ ਮੰਜ਼ਿਲ 'ਤੇ ਭੇਜ ਦਿੱਤਾ ਗਿਆ: {title}",
    "cancel_pending": "❌ ਬਾਕੀ ਸੈਟਿੰਗ ਰੱਦ ਕਰ ਦਿੱਤੀ ਗਈ।",
}

EXTRA_TRANSLATIONS["gu"] = {
    "settings_status": "⚙️ વપરાશકર્તા સેટિંગ્સ\n\nભાષા: {language}\nથંબનેલ: {thumb}\nમુકામ: {dest}",
    "dest_default": "ડિફોલ્ટ (આ ચેટ)",
    "thumb_set_prompt": "🖼️ કસ્ટમ થંબનેલ તરીકે સેટ કરવા હવે મને એક ફોટો મોકલો.",
    "thumb_invalid": "❌ એ ઇમેજ પ્રોસેસ કરી શકાઈ નહીં. કૃપા કરીને બીજો ફોટો મોકલો.",
    "thumb_set_done": "✅ કસ્ટમ થંબનેલ સેટ થયું.",
    "thumb_removed": "✅ કસ્ટમ થંબનેલ દૂર કર્યું.",
    "dest_set_prompt": "📥 હવે તમારી ચેનલ/ગ્રુપ આઈડી મોકલો (દા.ત. -1001234567890).",
    "dest_set_done": "✅ લીચ મુકામ સેટ: {title}",
    "dest_removed": "✅ લીચ મુકામ દૂર કર્યો. વિડિયો હવે આ ચેટમાં મોકલાશે.",
    "dest_invalid": "❌ ખોટી ચેનલ/ગ્રુપ આઈડી. તે -1001234567890 જેવી હોવી જોઈએ. ફરી પ્રયાસ માટે /user_settings મોકલો.",
    "dest_no_access": "❌ પહેલા મને એ ચેટમાં એડમિન બનાવો. મને એડમિન તરીકે ઉમેરો અને ફરી પ્રયાસ કરો.",
    "dest_not_admin": "❌ મુકામ તરીકે સેટ કરવા તમારે એ ચેટના એડમિન હોવા જોઈએ.",
    "dest_send_failed": "⚠️ તમારા મુકામે મોકલી શકાયું નહીં, એટલે અહીં મોકલ્યું.",
    "dest_delivered": "✅ વિડિયો તમારા મુકામે મોકલ્યો: {title}",
    "cancel_pending": "❌ બાકી સેટિંગ રદ કરી.",
}

EXTRA_TRANSLATIONS["es"] = {
    "settings_status": "⚙️ Ajustes de usuario\n\nIdioma: {language}\nMiniatura: {thumb}\nDestino: {dest}",
    "dest_default": "Predeterminado (este chat)",
    "thumb_set_prompt": "🖼️ Envíame ahora una foto para establecerla como miniatura personalizada.",
    "thumb_invalid": "❌ No se pudo procesar esa imagen. Envía otra foto.",
    "thumb_set_done": "✅ Miniatura personalizada establecida.",
    "thumb_removed": "✅ Miniatura personalizada eliminada.",
    "dest_set_prompt": "📥 Envíame ahora el ID de tu canal/grupo (p. ej. -1001234567890).",
    "dest_set_done": "✅ Destino establecido: {title}",
    "dest_removed": "✅ Destino eliminado. Los vídeos se enviarán a este chat.",
    "dest_invalid": "❌ ID de canal/grupo no válido. Debe ser como -1001234567890. Envía /user_settings para intentarlo de nuevo.",
    "dest_no_access": "❌ Primero debo ser administrador en ese chat. Agrégame como admin e inténtalo de nuevo.",
    "dest_not_admin": "❌ Debes ser administrador de ese chat para establecerlo como destino.",
    "dest_send_failed": "⚠️ No se pudo enviar a tu destino, así que lo envié aquí.",
    "dest_delivered": "✅ Vídeo entregado en tu destino: {title}",
    "cancel_pending": "❌ Configuración pendiente cancelada.",
}

EXTRA_TRANSLATIONS["fr"] = {
    "settings_status": "⚙️ Paramètres utilisateur\n\nLangue : {language}\nMiniature : {thumb}\nDestination : {dest}",
    "dest_default": "Par défaut (ce chat)",
    "thumb_set_prompt": "🖼️ Envoyez-moi maintenant une photo pour la définir comme miniature personnalisée.",
    "thumb_invalid": "❌ Impossible de traiter cette image. Envoyez une autre photo.",
    "thumb_set_done": "✅ Miniature personnalisée définie.",
    "thumb_removed": "✅ Miniature personnalisée supprimée.",
    "dest_set_prompt": "📥 Envoyez-moi maintenant l'ID de votre canal/groupe (ex. -1001234567890).",
    "dest_set_done": "✅ Destination définie : {title}",
    "dest_removed": "✅ Destination supprimée. Les vidéos seront envoyées dans ce chat.",
    "dest_invalid": "❌ ID de canal/groupe invalide. Il doit ressembler à -1001234567890. Envoyez /user_settings pour réessayer.",
    "dest_no_access": "❌ Je dois d'abord être administrateur dans ce chat. Ajoutez-moi comme admin et réessayez.",
    "dest_not_admin": "❌ Vous devez être administrateur de ce chat pour le définir comme destination.",
    "dest_send_failed": "⚠️ Impossible d'envoyer vers votre destination, je l'ai donc envoyé ici.",
    "dest_delivered": "✅ Vidéo livrée à votre destination : {title}",
    "cancel_pending": "❌ Réglage en attente annulé.",
}

EXTRA_TRANSLATIONS["de"] = {
    "settings_status": "⚙️ Benutzereinstellungen\n\nSprache: {language}\nVorschaubild: {thumb}\nZiel: {dest}",
    "dest_default": "Standard (dieser Chat)",
    "thumb_set_prompt": "🖼️ Sende mir jetzt ein Foto, um es als eigenes Vorschaubild festzulegen.",
    "thumb_invalid": "❌ Dieses Bild konnte nicht verarbeitet werden. Bitte sende ein anderes Foto.",
    "thumb_set_done": "✅ Eigenes Vorschaubild festgelegt.",
    "thumb_removed": "✅ Eigenes Vorschaubild entfernt.",
    "dest_set_prompt": "📥 Sende mir jetzt deine Kanal-/Gruppen-ID (z. B. -1001234567890).",
    "dest_set_done": "✅ Leech-Ziel festgelegt: {title}",
    "dest_removed": "✅ Leech-Ziel entfernt. Videos werden an diesen Chat gesendet.",
    "dest_invalid": "❌ Ungültige Kanal-/Gruppen-ID. Sie muss wie -1001234567890 aussehen. Sende /user_settings, um es erneut zu versuchen.",
    "dest_no_access": "❌ Ich muss zuerst Admin in diesem Chat sein. Füge mich als Admin hinzu und versuche es erneut.",
    "dest_not_admin": "❌ Du musst Admin dieses Chats sein, um es als Ziel festzulegen.",
    "dest_send_failed": "⚠️ Es konnte nicht an dein Ziel gesendet werden, daher habe ich es hierher gesendet.",
    "dest_delivered": "✅ Video an dein Ziel zugestellt: {title}",
    "cancel_pending": "❌ Ausstehende Einstellung abgebrochen.",
}

for _code, _extra in EXTRA_TRANSLATIONS.items():
    TRANSLATIONS[_code].update(_extra)

# Hint shown in the /start welcome message pointing users to settings.
WELCOME_SETTINGS_HINTS = {
    "en": "🌐 Send /user_settings anytime to change your language and more.",
    "hi": "🌐 अपनी भाषा और अन्य सेटिंग्स बदलने के लिए कभी भी /user_settings भेजें।",
    "mr": "🌐 तुमची भाषा आणि अधिक बदलण्यासाठी कधीही /user_settings पाठवा.",
    "bn": "🌐 আপনার ভাষা ও আরও সেটিংস বদলাতে যেকোনো সময় /user_settings পাঠান।",
    "ta": "🌐 உங்கள் மொழி மற்றும் பலவற்றை மாற்ற எப்போதும் /user_settings அனுப்புங்கள்.",
    "te": "🌐 మీ భాష మరియు మరిన్ని మార్చడానికి ఎప్పుడైనా /user_settings పంపండి.",
    "kn": "🌐 ನಿಮ್ಮ ಭಾಷೆ ಮತ್ತು ಹೆಚ್ಚಿನದನ್ನು ಬದಲಿಸಲು ಯಾವಾಗ ಬೇಕಾದರೂ /user_settings ಕಳುಹಿಸಿ.",
    "ml": "🌐 നിങ്ങളുടെ ഭാഷയും കൂടുതലും മാറ്റാൻ എപ്പോൾ വേണമെങ്കിലും /user_settings അയയ്ക്കുക.",
    "ur": "🌐 اپنی زبان اور مزید سیٹنگز بدلنے کے لیے کبھی بھی /user_settings بھیجیں۔",
    "pa": "🌐 ਆਪਣੀ ਭਾਸ਼ਾ ਅਤੇ ਹੋਰ ਬਦਲਣ ਲਈ ਕਦੇ ਵੀ /user_settings ਭੇਜੋ।",
    "gu": "🌐 તમારી ભાષા અને વધુ બદલવા માટે ગમે ત્યારે /user_settings મોકલો.",
    "es": "🌐 Envía /user_settings cuando quieras para cambiar tu idioma y más.",
    "fr": "🌐 Envoyez /user_settings à tout moment pour changer de langue et plus.",
    "de": "🌐 Sende jederzeit /user_settings, um deine Sprache und mehr zu ändern.",
}

for _code, _hint in WELCOME_SETTINGS_HINTS.items():
    TRANSLATIONS[_code]["welcome_settings"] = _hint

# Buttons in the /start welcome message.
START_BUTTON_TRANSLATIONS = {
    "en": {"btn_join": "Join ❤️🚀", "btn_developer": "Developer ⚡️", "btn_repo": "Repo 🌐"},
    "hi": {"btn_join": "जुड़ें ❤️🚀", "btn_developer": "डेवलपर ⚡️", "btn_repo": "रेपो 🌐"},
    "mr": {"btn_join": "सामील व्हा ❤️🚀", "btn_developer": "डेव्हलपर ⚡️", "btn_repo": "रेपो 🌐"},
    "bn": {"btn_join": "যোগ দিন ❤️🚀", "btn_developer": "ডেভেলপার ⚡️", "btn_repo": "রেপো 🌐"},
    "ta": {"btn_join": "சேரவும் ❤️🚀", "btn_developer": "டெவலப்பர் ⚡️", "btn_repo": "ரெப்போ 🌐"},
    "te": {"btn_join": "చేరండి ❤️🚀", "btn_developer": "డెవలపర్ ⚡️", "btn_repo": "రెపో 🌐"},
    "kn": {"btn_join": "ಸೇರಿ ❤️🚀", "btn_developer": "ಡೆವಲಪರ್ ⚡️", "btn_repo": "ರೆಪೊ 🌐"},
    "ml": {"btn_join": "ചേരുക ❤️🚀", "btn_developer": "ഡെവലപ്പർ ⚡️", "btn_repo": "റെപ്പോ 🌐"},
    "ur": {"btn_join": "شامل ہوں ❤️🚀", "btn_developer": "ڈویلپر ⚡️", "btn_repo": "ریپو 🌐"},
    "pa": {"btn_join": "ਸ਼ਾਮਲ ਹੋਵੋ ❤️🚀", "btn_developer": "ਡਿਵੈਲਪਰ ⚡️", "btn_repo": "ਰੈਪੋ 🌐"},
    "gu": {"btn_join": "જોડાઓ ❤️🚀", "btn_developer": "ડેવલપર ⚡️", "btn_repo": "રેપો 🌐"},
    "es": {"btn_join": "Unirse ❤️🚀", "btn_developer": "Desarrollador ⚡️", "btn_repo": "Repo 🌐"},
    "fr": {"btn_join": "Rejoindre ❤️🚀", "btn_developer": "Développeur ⚡️", "btn_repo": "Dépôt 🌐"},
    "de": {"btn_join": "Beitreten ❤️🚀", "btn_developer": "Entwickler ⚡️", "btn_repo": "Repo 🌐"},
}

for _code, _buttons in START_BUTTON_TRANSLATIONS.items():
    TRANSLATIONS[_code].update(_buttons)

# Additional languages: Italian, Japanese, Korean, Chinese.
ADDITIONAL_LANGUAGES = [
    ("it", "Italiano"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("zh", "中文"),
]

TRANSLATIONS["it"] = {
    "welcome": "🌟 {mention}, sono un bot downloader per Terabox. Inviami un qualsiasi link Terabox, lo scaricherò in pochi secondi e te lo invierò ✨.",
    "must_join": "Devi unirti al mio canale per usarmi.",
    "cooldown": "L'API è in sviluppo. Per ridurre gli abusi devi attendere {remaining}s.",
    "invalid_link": "Inserisci un link Terabox valido.",
    "sending_media": "Ti sto inviando il file...🤤",
    "download_failed": (
        "Download non riuscito ❌\n\n"
        "Motivo: il link potrebbe essere non valido o è un link a una cartella.\n"
        "Sono supportati solo i link ai file."
    ),
    "file_deleted_warning": "⚠️ Questo file verrà eliminato automaticamente tra 10 minuti. Inoltralo per salvarlo.",
    "no_videos": "Nessun video indicizzato. Il proprietario può usare /refresh per creare l'indice.",
    "mongo_missing": "MongoDB non è configurato.",
    "search_usage": "Uso: /search <da 1 a 3 parole chiave>",
    "search_no_results": "Nessun file trovato che corrisponda a tutte le parole chiave fornite.",
    "search_unavailable": "La ricerca non è disponibile al momento. Riprova.",
    "search_expired": "Questa ricerca è scaduta. Invia di nuovo /search.",
    "search_not_yours": "Questa ricerca appartiene a un altro utente.",
    "search_none_left": "Non ci sono più file corrispondenti disponibili.",
    "search_send_failed": "Impossibile inviare questo file. Potrebbe essere stato rimosso dal canale di origine.",
    "search_header": "🔎 Ricerca: {keywords}\nTrovati {count} file corrispondenti. Seleziona un nome file qui sotto.",
    "search_sending": "Invio del file...",
    "search_file_unavailable": "Questo file non è più disponibile.",
    "dump_caption": (
        "💾 Accesso permanente al canale dump\n\n"
        "Acquista l'accesso permanente all'intero canale dump.\n\n"
        "• Binance: solo 2,75 USDT\n"
        "• UPI: solo ₹250\n\n"
        "Scegli il metodo di pagamento qui sotto. Dopo il pagamento, invia lo "
        "screenshot a @rtx5069 per la verifica."
    ),
    "dump_qr_binance": (
        "Pagamento Binance\n\n"
        "Importo: solo 2,75 USDT\n\n"
        "Scansiona questo QR con l'app Binance. Dopo il pagamento, invia lo "
        "screenshot a @rtx5069 per la verifica."
    ),
    "dump_qr_upi": (
        "Pagamento UPI\n\n"
        "Importo: solo ₹250\n\n"
        "Scansiona questo QR con qualsiasi app UPI. Dopo il pagamento, invia "
        "lo screenshot a @rtx5069 per la verifica."
    ),
    "dump_qr_error": "Impossibile mostrare il QR di pagamento. Invia /dump e riprova.",
    "dump_unavailable": "Le informazioni di accesso al dump non sono disponibili al momento.",
    "dump_menu_unavailable": "Il menu di pagamento non è disponibile al momento.",
    "select_language": "🌐 Scegli la tua lingua:",
    "language_saved": "✅ Lingua impostata: {language}",
    "confirm": "✅ Conferma",
    "settings_title": "⚙️ Impostazioni utente",
    "settings_status": "⚙️ Impostazioni utente\n\nLingua: {language}\nMiniatura: {thumb}\nDestinazione: {dest}",
    "dest_default": "Predefinita (questa chat)",
    "thumb_set_prompt": "🖼️ Inviami ora una foto per impostarla come miniatura personalizzata.",
    "thumb_invalid": "❌ Impossibile elaborare quell'immagine. Invia un'altra foto.",
    "thumb_set_done": "✅ Miniatura personalizzata impostata.",
    "thumb_removed": "✅ Miniatura personalizzata rimossa.",
    "dest_set_prompt": "📥 Inviami ora l'ID del tuo canale/gruppo (es. -1001234567890).",
    "dest_set_done": "✅ Destinazione impostata: {title}",
    "dest_removed": "✅ Destinazione rimossa. I video verranno inviati a questa chat.",
    "dest_invalid": "❌ ID canale/gruppo non valido. Deve essere simile a -1001234567890. Invia /user_settings per riprovare.",
    "dest_no_access": "❌ Devo prima essere amministratore in quella chat. Aggiungimi come admin e riprova.",
    "dest_not_admin": "❌ Devi essere amministratore di quella chat per impostarla come destinazione.",
    "dest_send_failed": "⚠️ Impossibile inviare alla tua destinazione, quindi l'ho inviato qui.",
    "dest_delivered": "✅ Video consegnato alla tua destinazione: {title}",
    "cancel_pending": "❌ Impostazione in sospeso annullata.",
    "welcome_settings": "🌐 Invia /user_settings quando vuoi per cambiare lingua e altro.",
    "btn_join": "Unisciti ❤️🚀",
    "btn_developer": "Sviluppatore ⚡️",
    "btn_repo": "Repo 🌐",
}

TRANSLATIONS["ja"] = {
    "welcome": "🌟 {mention}、私は Terabox ダウンローダーボットです。Terabox のリンクを送ってください。数秒でダウンロードしてお送りします ✨。",
    "must_join": "私を使うにはチャンネルに参加してください。",
    "cooldown": "API は開発中です。悪用を防ぐため {remaining} 秒お待ちください。",
    "invalid_link": "有効な Terabox リンクを送ってください。",
    "sending_media": "メディアを送信しています...🤤",
    "download_failed": (
        "ダウンロードに失敗しました ❌\n\n"
        "理由: リンクが壊れているか、フォルダリンクの可能性があります。\n"
        "ファイルリンクのみ対応しています。"
    ),
    "file_deleted_warning": "⚠️ このファイルは10分後に自動削除されます。保存するには転送してください。",
    "no_videos": "まだ動画がインデックスされていません。オーナーは /refresh でインデックスを作成できます。",
    "mongo_missing": "MongoDB が設定されていません。",
    "search_usage": "使い方: /search <1〜3個のキーワード>",
    "search_no_results": "指定したすべてのキーワードに一致するファイルが見つかりませんでした。",
    "search_unavailable": "検索は一時的に利用できません。もう一度お試しください。",
    "search_expired": "この検索は期限切れです。/search をもう一度送信してください。",
    "search_not_yours": "この検索は別のユーザーのものです。",
    "search_none_left": "一致するファイルはもうありません。",
    "search_send_failed": "このファイルを送信できませんでした。ソースチャンネルから削除された可能性があります。",
    "search_header": "🔎 検索: {keywords}\n{count} 件の一致するファイルが見つかりました。下からファイル名を選択してください。",
    "search_sending": "ファイルを送信しています...",
    "search_file_unavailable": "このファイルはもう利用できません。",
    "dump_caption": (
        "💾 ダンプチャンネルへの永久アクセス\n\n"
        "ダンプチャンネル全体への永久アクセスを購入できます。\n\n"
        "• Binance: 2.75 USDT のみ\n"
        "• UPI: ₹250 のみ\n\n"
        "下から支払い方法を選択してください。支払い後、確認のためスクリーン"
        "ショットを @rtx5069 までお送りください。"
    ),
    "dump_qr_binance": (
        "Binance 支払い\n\n"
        "金額: 2.75 USDT のみ\n\n"
        "Binance アプリでこの QR をスキャンしてください。支払い後、確認の"
        "ためスクリーンショットを @rtx5069 までお送りください。"
    ),
    "dump_qr_upi": (
        "UPI 支払い\n\n"
        "金額: ₹250 のみ\n\n"
        "任意の UPI アプリでこの QR をスキャンしてください。支払い後、確認"
        "のためスクリーンショットを @rtx5069 までお送りください。"
    ),
    "dump_qr_error": "支払い QR を表示できませんでした。/dump を送信して再試行してください。",
    "dump_unavailable": "ダンプアクセス情報は一時的に利用できません。",
    "dump_menu_unavailable": "支払いメニューは一時的に利用できません。",
    "select_language": "🌐 言語を選択してください:",
    "language_saved": "✅ 言語を設定しました: {language}",
    "confirm": "✅ 確認",
    "settings_title": "⚙️ ユーザー設定",
    "settings_status": "⚙️ ユーザー設定\n\n言語: {language}\nサムネイル: {thumb}\n宛先: {dest}",
    "dest_default": "デフォルト (このチャット)",
    "thumb_set_prompt": "🖼️ カスタムサムネイルとして設定する写真を今すぐ送ってください。",
    "thumb_invalid": "❌ その画像を処理できませんでした。別の写真を送ってください。",
    "thumb_set_done": "✅ カスタムサムネイルを設定しました。",
    "thumb_removed": "✅ カスタムサムネイルを削除しました。",
    "dest_set_prompt": "📥 チャンネル/グループ ID を送ってください (例: -1001234567890)。",
    "dest_set_done": "✅ 保存先を設定しました: {title}",
    "dest_removed": "✅ 保存先を削除しました。動画はこのチャットに送信されます。",
    "dest_invalid": "❌ 無効なチャンネル/グループ ID です。-1001234567890 のような形式で送ってください。再試行するには /user_settings を送信してください。",
    "dest_no_access": "❌ まずそのチャットで管理者になる必要があります。管理者として追加してから再試行してください。",
    "dest_not_admin": "❌ 保存先として設定するには、そのチャットの管理者である必要があります。",
    "dest_send_failed": "⚠️ 保存先に送信できなかったため、ここに送信しました。",
    "dest_delivered": "✅ 動画を保存先に配信しました: {title}",
    "cancel_pending": "❌ 保留中の設定をキャンセルしました。",
    "welcome_settings": "🌐 言語などを変更するには、いつでも /user_settings を送信してください。",
    "btn_join": "参加 ❤️🚀",
    "btn_developer": "開発者 ⚡️",
    "btn_repo": "リポジトリ 🌐",
}

TRANSLATIONS["ko"] = {
    "welcome": "🌟 {mention}, 저는 Terabox 다운로더 봇입니다. 아무 Terabox 링크나 보내주세요. 몇 초 안에 다운로드해서 보내드리겠습니다 ✨.",
    "must_join": "저를 사용하려면 채널에 가입해야 합니다.",
    "cooldown": "API가 개발 중입니다. 남용을 줄이기 위해 {remaining}초 기다려야 합니다.",
    "invalid_link": "유효한 Terabox 링크를 보내주세요.",
    "sending_media": "미디어를 보내는 중...🤤",
    "download_failed": (
        "다운로드 실패 ❌\n\n"
        "이유: 링크가 손상되었거나 폴더 링크일 수 있습니다.\n"
        "파일 링크만 지원됩니다."
    ),
    "file_deleted_warning": "⚠️ 이 파일은 10분 후 자동으로 삭제됩니다. 저장하려면 전달하세요.",
    "no_videos": "아직 인덱싱된 동영상이 없습니다. 소유자는 /refresh로 인덱스를 만들 수 있습니다.",
    "mongo_missing": "MongoDB가 구성되지 않았습니다.",
    "search_usage": "사용법: /search <1~3개의 키워드>",
    "search_no_results": "제공한 모든 키워드와 일치하는 파일이 없습니다.",
    "search_unavailable": "검색을 일시적으로 사용할 수 없습니다. 다시 시도해 주세요.",
    "search_expired": "이 검색이 만료되었습니다. /search를 다시 보내세요.",
    "search_not_yours": "이 검색은 다른 사용자의 것입니다.",
    "search_none_left": "더 이상 일치하는 파일이 없습니다.",
    "search_send_failed": "이 파일을 보내지 못했습니다. 원본 채널에서 삭제되었을 수 있습니다.",
    "search_header": "🔎 검색: {keywords}\n{count}개의 일치하는 파일을 찾았습니다. 아래에서 파일명을 선택하세요.",
    "search_sending": "파일을 보내는 중...",
    "search_file_unavailable": "이 파일은 더 이상 사용할 수 없습니다.",
    "dump_caption": (
        "💾 덤프 채널 영구 이용권\n\n"
        "덤프 채널 전체에 대한 영구 이용권을 구매하세요.\n\n"
        "• Binance: 2.75 USDT만\n"
        "• UPI: ₹250만\n\n"
        "아래에서 결제 방법을 선택하세요. 결제 후 확인을 위해 스크린샷을 "
        "@rtx5069로 보내주세요."
    ),
    "dump_qr_binance": (
        "Binance 결제\n\n"
        "금액: 2.75 USDT만\n\n"
        "Binance 앱으로 이 QR을 스캔하세요. 결제 후 확인을 위해 스크린샷을 "
        "@rtx5069로 보내주세요."
    ),
    "dump_qr_upi": (
        "UPI 결제\n\n"
        "금액: ₹250만\n\n"
        "아무 UPI 앱으로 이 QR을 스캔하세요. 결제 후 확인을 위해 스크린샷을 "
        "@rtx5069로 보내주세요."
    ),
    "dump_qr_error": "결제 QR을 표시할 수 없습니다. /dump를 보내고 다시 시도하세요.",
    "dump_unavailable": "덤프 이용 정보를 일시적으로 사용할 수 없습니다.",
    "dump_menu_unavailable": "결제 메뉴를 일시적으로 사용할 수 없습니다.",
    "select_language": "🌐 언어를 선택하세요:",
    "language_saved": "✅ 언어가 설정되었습니다: {language}",
    "confirm": "✅ 확인",
    "settings_title": "⚙️ 사용자 설정",
    "settings_status": "⚙️ 사용자 설정\n\n언어: {language}\n썸네일: {thumb}\n대상: {dest}",
    "dest_default": "기본 (이 채팅)",
    "thumb_set_prompt": "🖼️ 사용자 지정 썸네일로 설정할 사진을 지금 보내주세요.",
    "thumb_invalid": "❌ 해당 이미지를 처리할 수 없습니다. 다른 사진을 보내주세요.",
    "thumb_set_done": "✅ 사용자 지정 썸네일이 설정되었습니다.",
    "thumb_removed": "✅ 사용자 지정 썸네일이 제거되었습니다.",
    "dest_set_prompt": "📥 채널/그룹 ID를 보내주세요 (예: -1001234567890).",
    "dest_set_done": "✅ 대상이 설정되었습니다: {title}",
    "dest_removed": "✅ 대상이 제거되었습니다. 동영상은 이 채팅으로 전송됩니다.",
    "dest_invalid": "❌ 잘못된 채널/그룹 ID입니다. -1001234567890 형식이어야 합니다. 다시 시도하려면 /user_settings를 보내세요.",
    "dest_no_access": "❌ 먼저 해당 채팅에서 관리자여야 합니다. 관리자로 추가한 후 다시 시도하세요.",
    "dest_not_admin": "❌ 대상을 설정하려면 해당 채팅의 관리자여야 합니다.",
    "dest_send_failed": "⚠️ 대상으로 보내지 못해 여기로 보냈습니다.",
    "dest_delivered": "✅ 동영상이 대상으로 전달되었습니다: {title}",
    "cancel_pending": "❌ 대기 중인 설정이 취소되었습니다.",
    "welcome_settings": "🌐 언어 등을 변경하려면 언제든지 /user_settings를 보내세요.",
    "btn_join": "참여 ❤️🚀",
    "btn_developer": "개발자 ⚡️",
    "btn_repo": "저장소 🌐",
}

TRANSLATIONS["zh"] = {
    "welcome": "🌟 {mention}，我是一个 Terabox 下载机器人。把任意 Terabox 链接发给我，我会在几秒内下载并发送给你 ✨。",
    "must_join": "你必须加入我的频道才能使用我。",
    "cooldown": "API 仍在开发中。为减少滥用，请等待 {remaining} 秒。",
    "invalid_link": "请提供有效的 Terabox 链接。",
    "sending_media": "正在发送媒体...🤤",
    "download_failed": (
        "下载失败 ❌\n\n"
        "原因：链接可能已失效，或者是文件夹链接。\n"
        "仅支持文件链接。"
    ),
    "file_deleted_warning": "⚠️ 此文件将在 10 分钟后自动删除。请转发以保存。",
    "no_videos": "尚未收录视频。所有者可以使用 /refresh 建立索引。",
    "mongo_missing": "未配置 MongoDB。",
    "search_usage": "用法：/search <1 到 3 个关键词>",
    "search_no_results": "未找到匹配所有关键词的文件。",
    "search_unavailable": "搜索暂时不可用，请重试。",
    "search_expired": "此搜索已过期。请重新发送 /search。",
    "search_not_yours": "此搜索属于其他用户。",
    "search_none_left": "没有更多匹配的文件了。",
    "search_send_failed": "发送此文件失败，可能已被从源频道移除。",
    "search_header": "🔎 搜索：{keywords}\n找到 {count} 个匹配文件。请在下方选择文件名。",
    "search_sending": "正在发送文件...",
    "search_file_unavailable": "此文件已不可用。",
    "dump_caption": (
        "💾 永久转储频道访问权限\n\n"
        "购买整个转储频道的永久访问权限。\n\n"
        "• Binance：仅 2.75 USDT\n"
        "• UPI：仅 ₹250\n\n"
        "请在下方选择支付方式。支付后，请将付款截图发送至 @rtx5069 "
        "进行验证。"
    ),
    "dump_qr_binance": (
        "Binance 付款\n\n"
        "金额：仅 2.75 USDT\n\n"
        "使用 Binance 应用扫描此二维码。支付后，请将截图发送至 "
        "@rtx5069 进行验证。"
    ),
    "dump_qr_upi": (
        "UPI 付款\n\n"
        "金额：仅 ₹250\n\n"
        "使用任意 UPI 应用扫描此二维码。支付后，请将截图发送至 "
        "@rtx5069 进行验证。"
    ),
    "dump_qr_error": "无法显示付款二维码。请发送 /dump 后重试。",
    "dump_unavailable": "转储访问信息暂时不可用。",
    "dump_menu_unavailable": "付款菜单暂时不可用。",
    "select_language": "🌐 选择你的语言：",
    "language_saved": "✅ 语言已设置：{language}",
    "confirm": "✅ 确认",
    "settings_title": "⚙️ 用户设置",
    "settings_status": "⚙️ 用户设置\n\n语言：{language}\n缩略图：{thumb}\n目标：{dest}",
    "dest_default": "默认（当前聊天）",
    "thumb_set_prompt": "🖼️ 现在发送一张照片，将其设置为自定义缩略图。",
    "thumb_invalid": "❌ 无法处理该图片。请发送另一张照片。",
    "thumb_set_done": "✅ 自定义缩略图已设置。",
    "thumb_removed": "✅ 自定义缩略图已移除。",
    "dest_set_prompt": "📥 现在发送你的频道/群组 ID（例如 -1001234567890）。",
    "dest_set_done": "✅ 目标已设置：{title}",
    "dest_removed": "✅ 目标已移除。视频将发送到此聊天。",
    "dest_invalid": "❌ 无效的频道/群组 ID。格式应类似 -1001234567890。请发送 /user_settings 重试。",
    "dest_no_access": "❌ 我需要先成为该聊天的管理员。请将我添加为管理员后重试。",
    "dest_not_admin": "❌ 你必须该聊天的管理员才能将其设为目标。",
    "dest_send_failed": "⚠️ 无法发送到你的目标，因此已发送到此处。",
    "dest_delivered": "✅ 视频已发送到你的目标：{title}",
    "cancel_pending": "❌ 已取消待处理的设置。",
    "welcome_settings": "🌐 随时发送 /user_settings 更改语言等设置。",
    "btn_join": "加入 ❤️🚀",
    "btn_developer": "开发者 ⚡️",
    "btn_repo": "仓库 🌐",
}

# Folder delivery settings (added in one block so every language stays in sync).
FOLDER_TRANSLATIONS = {
    "en": {
        "folder_current": "Folder: {mode}",
        "folder_settings": "📁 Folder Settings\n\nChoose how folder links are delivered:",
        "folder_zip": "🗜️ Zipped",
        "folder_single": "📄 Single files",
        "folder_saved": "✅ Folder mode set: {mode}",
        "folder_empty": "❌ No downloadable files found in this folder.",
        "folder_done": "📁 Folder complete\n✅ Files sent: {sent}\n⚠️ Skipped: {skipped}\n❌ Failed: {failed}",
    },
    "hi": {
        "folder_current": "फ़ोल्डर: {mode}",
        "folder_settings": "📁 फ़ोल्डर सेटिंग्स\n\nफ़ोल्डर लिंक कैसे भेजे जाएँ चुनें:",
        "folder_zip": "🗜️ ज़िप",
        "folder_single": "📄 अलग फ़ाइलें",
        "folder_saved": "✅ फ़ोल्डर मोड सेट: {mode}",
        "folder_empty": "❌ इस फ़ोल्डर में कोई डाउनलोड योग्य फ़ाइल नहीं मिली।",
        "folder_done": "📁 फ़ोल्डर पूरा\n✅ भेजी गई फ़ाइलें: {sent}\n⚠️ छोड़ी गई: {skipped}\n❌ विफल: {failed}",
    },
    "mr": {
        "folder_current": "फोल्डर: {mode}",
        "folder_settings": "📁 फोल्डर सेटिंग्ज\n\nफोल्डर लिंक कसे पाठवायचे ते निवडा:",
        "folder_zip": "🗜️ झिप",
        "folder_single": "📄 वेगळ्या फाइल्स",
        "folder_saved": "✅ फोल्डर मोड सेट: {mode}",
        "folder_empty": "❌ या फोल्डरमध्ये डाउनलोड करण्यायोग्य फाइल्स आढळल्या नाहीत.",
        "folder_done": "📁 फोल्डर पूर्ण\n✅ पाठवल्या: {sent}\n⚠️ वगळल्या: {skipped}\n❌ अयशस्वी: {failed}",
    },
    "bn": {
        "folder_current": "ফোল্ডার: {mode}",
        "folder_settings": "📁 ফোল্ডার সেটিংস\n\nফোল্ডার লিঙ্ক কীভাবে পাঠাতে হবে চুনুন:",
        "folder_zip": "🗜️ জিপ",
        "folder_single": "📄 আলাদা ফাইল",
        "folder_saved": "✅ ফোল্ডার মোড সেট: {mode}",
        "folder_empty": "❌ এই ফোল্ডারে কোনো ডাউনলোডযোগ্য ফাইল পাওয়া যায়নি।",
        "folder_done": "📁 ফোল্ডার সম্পন্ন\n✅ পাঠানো ফাইল: {sent}\n⚠️ বাদ দেওয়া: {skipped}\n❌ ব্যর্থ: {failed}",
    },
    "ta": {
        "folder_current": "கோப்புறை: {mode}",
        "folder_settings": "📁 கோப்புறை அமைப்புகள்\n\nகோப்புறை இணைப்புகளை எவ்வாறு அனுப்ப வேண்டும் என்பதைத் தேர்ந்தெடுக்கவும்:",
        "folder_zip": "🗜️ ஜிப்",
        "folder_single": "📄 தனி கோப்புகள்",
        "folder_saved": "✅ கோப்புறை முறை அமைக்கப்பட்டது: {mode}",
        "folder_empty": "❌ இந்தக் கோப்புறையில் பதிவிறக்கக்கூடிய கோப்புகள் இல்லை.",
        "folder_done": "📁 கோப்புறை முடிந்தது\n✅ அனுப்பியவை: {sent}\n⚠️ தவிர்த்தவை: {skipped}\n❌ தோல்வி: {failed}",
    },
    "te": {
        "folder_current": "ఫోల్డర్: {mode}",
        "folder_settings": "📁 ఫోల్డర్ సెట్టింగ్‌లు\n\nఫోల్డర్ లింక్‌లను ఎలా పంపాలో ఎంచుకోండి:",
        "folder_zip": "🗜️ జిప్",
        "folder_single": "📄 వేరే ఫైల్‌లు",
        "folder_saved": "✅ ఫోల్డర్ మోడ్ సెట్: {mode}",
        "folder_empty": "❌ ఈ ఫోల్డర్‌లో డౌన్‌లోడ్ చేయగల ఫైల్‌లు లేవు.",
        "folder_done": "📁 ఫోల్డర్ పూర్తయింది\n✅ పంపినవి: {sent}\n⚠️ దాటవేసినవి: {skipped}\n❌ విఫలమైనవి: {failed}",
    },
    "kn": {
        "folder_current": "ಫೋಲ್ಡರ್: {mode}",
        "folder_settings": "📁 ಫೋಲ್ಡರ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳು\n\nಫೋಲ್ಡರ್ ಲಿಂಕ್‌ಗಳನ್ನು ಹೇಗೆ ಕಳುಹಿಸಬೇಕೆಂದು ಆಯ್ಕೆಮಾಡಿ:",
        "folder_zip": "🗜️ ಜಿಪ್",
        "folder_single": "📄 ಪ್ರತ್ಯೇಕ ಫೈಲ್‌ಗಳು",
        "folder_saved": "✅ ಫೋಲ್ಡರ್ ಮೋಡ್ ಸೆಟ್: {mode}",
        "folder_empty": "❌ ಈ ಫೋಲ್ಡರ್‌ನಲ್ಲಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಬಹುದಾದ ಫೈಲ್‌ಗಳಿಲ್ಲ.",
        "folder_done": "📁 ಫೋಲ್ಡರ್ ಪೂರ್ಣಗೊಂಡಿದೆ\n✅ ಕಳುಹಿಸಿದವು: {sent}\n⚠️ ಬಿಟ್ಟುಬಿಟ್ಟವು: {skipped}\n❌ ವಿಫಲವಾದವು: {failed}",
    },
    "ml": {
        "folder_current": "ഫോൾഡർ: {mode}",
        "folder_settings": "📁 ഫോൾഡർ ക്രമീകരണങ്ങൾ\n\nഫോൾഡർ ലിങ്കുകൾ എങ്ങനെ അയയ്ക്കണമെന്ന് തിരഞ്ഞെടുക്കുക:",
        "folder_zip": "🗜️ സിപ്പ്",
        "folder_single": "📄 വെവ്വേറെ ഫയലുകൾ",
        "folder_saved": "✅ ഫോൾഡർ മോഡ് സെറ്റ്: {mode}",
        "folder_empty": "❌ ഈ ഫോൾഡറിൽ ഡൗൺലോഡ് ചെയ്യാവുന്ന ഫയലുകളില്ല.",
        "folder_done": "📁 ഫോൾഡർ പൂർത്തിയായി\n✅ അയച്ചവ: {sent}\n⚠️ ഒഴിവാക്കിയവ: {skipped}\n❌ പരാജയപ്പെട്ടവ: {failed}",
    },
    "ur": {
        "folder_current": "فولڈر: {mode}",
        "folder_settings": "📁 فولڈر سیٹنگز\n\nفولڈر لنکس کیسے بھیجے جائیں منتخب کریں:",
        "folder_zip": "🗜️ زپ",
        "folder_single": "📄 الگ فائلیں",
        "folder_saved": "✅ فولڈر موڈ سیٹ: {mode}",
        "folder_empty": "❌ اس فولڈر میں کوئی ڈاؤن لوڈ کے قابل فائل نہیں ملی۔",
        "folder_done": "📁 فولڈر مکمل\n✅ بھیجی گئی فائلیں: {sent}\n⚠️ چھوڑی گئیں: {skipped}\n❌ ناکام: {failed}",
    },
    "pa": {
        "folder_current": "ਫੋਲਡਰ: {mode}",
        "folder_settings": "📁 ਫੋਲਡਰ ਸੈਟਿੰਗਾਂ\n\nਫੋਲਡਰ ਲਿੰਕ ਕਿਵੇਂ ਭੇਜਣੇ ਹਨ ਚੁਣੋ:",
        "folder_zip": "🗜️ ਜ਼ਿਪ",
        "folder_single": "📄 ਵੱਖਰੀਆਂ ਫਾਈਲਾਂ",
        "folder_saved": "✅ ਫੋਲਡਰ ਮੋਡ ਸੈੱਟ: {mode}",
        "folder_empty": "❌ ਇਸ ਫੋਲਡਰ ਵਿੱਚ ਕੋਈ ਡਾਊਨਲੋਡ ਯੋਗ ਫਾਈਲ ਨਹੀਂ ਮਿਲੀ।",
        "folder_done": "📁 ਫੋਲਡਰ ਪੂਰਾ\n✅ ਭੇਜੀਆਂ: {sent}\n⚠️ ਛੱਡੀਆਂ: {skipped}\n❌ ਅਸਫਲ: {failed}",
    },
    "gu": {
        "folder_current": "ફોલ્ડર: {mode}",
        "folder_settings": "📁 ફોલ્ડર સેટિંગ્સ\n\nફોલ્ડર લિંક કેવી રીતે મોકલવી તે પસંદ કરો:",
        "folder_zip": "🗜️ ઝિપ",
        "folder_single": "📄 અલગ ફાઇલો",
        "folder_saved": "✅ ફોલ્ડર મોડ સેટ: {mode}",
        "folder_empty": "❌ આ ફોલ્ડરમાં ડાઉનલોડ કરી શકાય તેવી કોઈ ફાઇલ મળી નથી.",
        "folder_done": "📁 ફોલ્ડર પૂર્ણ\n✅ મોકલેલી: {sent}\n⚠️ છોડેલી: {skipped}\n❌ નિષ્ફળ: {failed}",
    },
    "es": {
        "folder_current": "Carpeta: {mode}",
        "folder_settings": "📁 Ajustes de carpeta\n\nElige cómo se envían los enlaces de carpeta:",
        "folder_zip": "🗜️ Comprimido",
        "folder_single": "📄 Archivos individuales",
        "folder_saved": "✅ Modo de carpeta: {mode}",
        "folder_empty": "❌ No se encontraron archivos descargables en esta carpeta.",
        "folder_done": "📁 Carpeta completada\n✅ Enviados: {sent}\n⚠️ Omitidos: {skipped}\n❌ Fallidos: {failed}",
    },
    "fr": {
        "folder_current": "Dossier : {mode}",
        "folder_settings": "📁 Paramètres des dossiers\n\nChoisissez comment les liens de dossier sont envoyés :",
        "folder_zip": "🗜️ Compressé",
        "folder_single": "📄 Fichiers individuels",
        "folder_saved": "✅ Mode dossier défini : {mode}",
        "folder_empty": "❌ Aucun fichier téléchargeable trouvé dans ce dossier.",
        "folder_done": "📁 Dossier terminé\n✅ Envoyés : {sent}\n⚠️ Ignorés : {skipped}\n❌ Échoués : {failed}",
    },
    "de": {
        "folder_current": "Ordner: {mode}",
        "folder_settings": "📁 Ordner-Einstellungen\n\nWähle, wie Ordner-Links gesendet werden:",
        "folder_zip": "🗜️ Gezippt",
        "folder_single": "📄 Einzelne Dateien",
        "folder_saved": "✅ Ordnermodus gesetzt: {mode}",
        "folder_empty": "❌ In diesem Ordner wurden keine herunterladbaren Dateien gefunden.",
        "folder_done": "📁 Ordner abgeschlossen\n✅ Gesendet: {sent}\n⚠️ Übersprungen: {skipped}\n❌ Fehlgeschlagen: {failed}",
    },
    "it": {
        "folder_current": "Cartella: {mode}",
        "folder_settings": "📁 Impostazioni cartella\n\nScegli come inviare i link delle cartelle:",
        "folder_zip": "🗜️ Zippato",
        "folder_single": "📄 File singoli",
        "folder_saved": "✅ Modalità cartella impostata: {mode}",
        "folder_empty": "❌ Nessun file scaricabile trovato in questa cartella.",
        "folder_done": "📁 Cartella completata\n✅ Inviati: {sent}\n⚠️ Saltati: {skipped}\n❌ Non riusciti: {failed}",
    },
    "ja": {
        "folder_current": "フォルダー: {mode}",
        "folder_settings": "📁 フォルダー設定\n\nフォルダーリンクの送信方法を選択してください:",
        "folder_zip": "🗜️ ZIP",
        "folder_single": "📄 個別ファイル",
        "folder_saved": "✅ フォルダーモードを設定しました: {mode}",
        "folder_empty": "❌ このフォルダーにダウンロード可能なファイルがありません。",
        "folder_done": "📁 フォルダー完了\n✅ 送信: {sent}\n⚠️ スキップ: {skipped}\n❌ 失敗: {failed}",
    },
    "ko": {
        "folder_current": "폴더: {mode}",
        "folder_settings": "📁 폴더 설정\n\n폴더 링크를 보낼 방식을 선택하세요:",
        "folder_zip": "🗜️ 압축 파일",
        "folder_single": "📄 개별 파일",
        "folder_saved": "✅ 폴더 모드를 설정했습니다: {mode}",
        "folder_empty": "❌ 이 폴더에서 다운로드 가능한 파일을 찾지 못했습니다.",
        "folder_done": "📁 폴더 완료\n✅ 전송: {sent}\n⚠️ 건너뜀: {skipped}\n❌ 실패: {failed}",
    },
    "zh": {
        "folder_current": "文件夹：{mode}",
        "folder_settings": "📁 文件夹设置\n\n选择文件夹链接的发送方式：",
        "folder_zip": "🗜️ 压缩包",
        "folder_single": "📄 单个文件",
        "folder_saved": "✅ 文件夹模式已设置：{mode}",
        "folder_empty": "❌ 此文件夹中没有可下载的文件。",
        "folder_done": "📁 文件夹处理完成\n✅ 已发送：{sent}\n⚠️ 已跳过：{skipped}\n❌ 失败：{failed}",
    },
}

for _code, _extra in FOLDER_TRANSLATIONS.items():
    TRANSLATIONS[_code].update(_extra)

for _code, _name in ADDITIONAL_LANGUAGES:
    assert _code in TRANSLATIONS, f"missing translations for {_code}"

LANGUAGES.extend(ADDITIONAL_LANGUAGES)
LANGUAGE_CODES = {code for code, _name in LANGUAGES}

PREMIUM_TRANSLATIONS = {
    "en": {
        "welcome_plans": "🆓 Free tier: 10 downloads, 10 /random and 10 /search per day. Folder downloads are premium.\n⭐ Use /subscribe for unlimited access.",
        "limit_terabox": "⏳ Daily limit reached — {limit} TeraBox files per day.\n\nResets in {reset} at 12:00 AM IST.\nUpgrade with /subscribe for unlimited downloads.",
        "limit_random": "⏳ Daily limit reached — {limit} /random uses per day.\n\nResets in {reset} at 12:00 AM IST.\nUpgrade with /subscribe for unlimited use.",
        "limit_search": "⏳ Daily limit reached — {limit} /search uses per day.\n\nResets in {reset} at 12:00 AM IST.\nUpgrade with /subscribe for unlimited use.",
        "quota_left": "📊 {remaining} free uses left today. Resets in {reset} at 12:00 AM IST.",
        "folder_premium": "📁 Folder downloads are a premium feature.\n\nUpgrade with /subscribe to unlock folder downloads, unlimited downloads, /random and /search.",
    },
    "hi": {
        "welcome_plans": "🆓 मुफ़्त सीमा: प्रतिदिन 10 डाउनलोड, 10 /random और 10 /search। फ़ोल्डर डाउनलोड प्रीमियम हैं।\n⭐ असीमित उपयोग के लिए /subscribe करें।",
        "limit_terabox": "⏳ दैनिक सीमा पूरी — प्रतिदिन {limit} TeraBox फ़ाइलें।\n\n{reset} में 12:00 AM IST पर रीसेट होगी।\nअसीमित डाउनलोड के लिए /subscribe करें।",
        "limit_random": "⏳ दैनिक सीमा पूरी — प्रतिदिन {limit} /random उपयोग।\n\n{reset} में 12:00 AM IST पर रीसेट होगी।\nअसीमित उपयोग के लिए /subscribe करें।",
        "limit_search": "⏳ दैनिक सीमा पूरी — प्रतिदिन {limit} /search उपयोग।\n\n{reset} में 12:00 AM IST पर रीसेट होगी।\nअसीमित उपयोग के लिए /subscribe करें।",
        "quota_left": "📊 आज {remaining} मुफ़्त उपयोग शेष। {reset} में 12:00 AM IST पर रीसेट होगा।",
        "folder_premium": "📁 फ़ोल्डर डाउनलोड प्रीमियम सुविधा है।\n\nफ़ोल्डर, असीमित डाउनलोड, /random और /search के लिए /subscribe करें।",
    },
    "mr": {
        "welcome_plans": "🆓 मोफत मर्यादा: दररोज 10 डाउनलोड, 10 /random आणि 10 /search. फोल्डर डाउनलोड प्रीमियम आहेत.\n⭐ अमर्यादित वापरासाठी /subscribe करा.",
        "limit_terabox": "⏳ दैनिक मर्यादा पूर्ण — दररोज {limit} TeraBox फाइली.\n\n{reset} मध्ये 12:00 AM IST ला रीसेट होईल.\nअमर्यादित डाउनलोडसाठी /subscribe करा.",
        "limit_random": "⏳ दैनिक मर्यादा पूर्ण — दररोज {limit} /random वापर.\n\n{reset} मध्ये 12:00 AM IST ला रीसेट होईल.\nअमर्यादित वापरासाठी /subscribe करा.",
        "limit_search": "⏳ दैनिक मर्यादा पूर्ण — दररोज {limit} /search वापर.\n\n{reset} मध्ये 12:00 AM IST ला रीसेट होईल.\nअमर्यादित वापरासाठी /subscribe करा.",
        "quota_left": "📊 आज {remaining} मोफत वापर शिल्लक. {reset} मध्ये 12:00 AM IST ला रीसेट होईल.",
        "folder_premium": "📁 फोल्डर डाउनलोड प्रीमियम सुविधा आहे.\n\nफोल्डर, अमर्यादित डाउनलोड, /random आणि /search साठी /subscribe करा.",
    },
    "bn": {
        "welcome_plans": "🆓 বিনামূল্যের সীমা: প্রতিদিন 10 ডাউনলোড, 10 /random এবং 10 /search। ফোল্ডার ডাউনলোড প্রিমিয়াম।\n⭐ আনলিমিটেড ব্যবহারের জন্য /subscribe করুন।",
        "limit_terabox": "⏳ দৈনিক সীমা শেষ — প্রতিদিন {limit} TeraBox ফাইল।\n\n{reset} পরে 12:00 AM IST-এ রিসেট হবে।\nআনলিমিটেড ডাউনলোডের জন্য /subscribe করুন।",
        "limit_random": "⏳ দৈনিক সীমা শেষ — প্রতিদিন {limit} /random ব্যবহার।\n\n{reset} পরে 12:00 AM IST-এ রিসেট হবে।\nআনলিমিটেড ব্যবহারের জন্য /subscribe করুন।",
        "limit_search": "⏳ দৈনিক সীমা শেষ — প্রতিদিন {limit} /search ব্যবহার।\n\n{reset} পরে 12:00 AM IST-এ রিসেট হবে।\nআনলিমিটেড ব্যবহারের জন্য /subscribe করুন।",
        "quota_left": "📊 আজ {remaining}টি বিনামূল্যের ব্যবহার বাকি। {reset} পরে 12:00 AM IST-এ রিসেট হবে।",
        "folder_premium": "📁 ফোল্ডার ডাউনলোড একটি প্রিমিয়াম সুবিধা।\n\nফোল্ডার, আনলিমিটেড ডাউনলোড, /random এবং /search-এর জন্য /subscribe করুন।",
    },
    "ta": {
        "welcome_plans": "🆓 இலவச வரம்பு: நாளொன்றுக்கு 10 பதிவிறக்கங்கள், 10 /random மற்றும் 10 /search. கோப்புறை பதிவிறக்கம் பிரீமியம்.\n⭐ வரம்பற்ற பயன்பாட்டிற்கு /subscribe செய்யுங்கள்.",
        "limit_terabox": "⏳ தினசரி வரம்பு முடிந்தது — நாளொன்றுக்கு {limit} TeraBox கோப்புகள்.\n\n{reset} இல் 12:00 AM IST-க்கு மீட்டமைக்கப்படும்.\nவரம்பற்ற பதிவிறக்கத்திற்கு /subscribe செய்யுங்கள்.",
        "limit_random": "⏳ தினசரி வரம்பு முடிந்தது — நாளொன்றுக்கு {limit} /random பயன்பாடுகள்.\n\n{reset} இல் 12:00 AM IST-க்கு மீட்டமைக்கப்படும்.\nவரம்பற்ற பயன்பாட்டிற்கு /subscribe செய்யுங்கள்.",
        "limit_search": "⏳ தினசரி வரம்பு முடிந்தது — நாளொன்றுக்கு {limit} /search பயன்பாடுகள்.\n\n{reset} இல் 12:00 AM IST-க்கு மீட்டமைக்கப்படும்.\nவரம்பற்ற பயன்பாட்டிற்கு /subscribe செய்யுங்கள்.",
        "quota_left": "📊 இன்று {remaining} இலவச பயன்பாடுகள் மீதம். {reset} இல் 12:00 AM IST-க்கு மீட்டமைக்கப்படும்.",
        "folder_premium": "📁 கோப்புறை பதிவிறக்கம் பிரீமியம் அம்சம்.\n\nகோப்புறை, வரம்பற்ற பதிவிறக்கம், /random மற்றும் /search-க்கு /subscribe செய்யுங்கள்.",
    },
    "te": {
        "welcome_plans": "🆓 ఉచిత పరిమితి: రోజుకు 10 డౌన్‌లోడ్‌లు, 10 /random మరియు 10 /search. ఫోల్డర్ డౌన్‌లోడ్‌లు ప్రీమియం.\n⭐ అపరిమిత వినియోగానికి /subscribe చేయండి.",
        "limit_terabox": "⏳ రోజువారీ పరిమితి ముగిసింది — రోజుకు {limit} TeraBox ఫైల్‌లు.\n\n{reset} లో 12:00 AM ISTకి రీసెట్ అవుతుంది.\nఅపరిమిత డౌన్‌లోడ్‌లకు /subscribe చేయండి.",
        "limit_random": "⏳ రోజువారీ పరిమితి ముగిసింది — రోజుకు {limit} /random వినియోగాలు.\n\n{reset} లో 12:00 AM ISTకి రీసెట్ అవుతుంది.\nఅపరిమిత వినియోగానికి /subscribe చేయండి.",
        "limit_search": "⏳ రోజువారీ పరిమితి ముగిసింది — రోజుకు {limit} /search వినియోగాలు.\n\n{reset} లో 12:00 AM ISTకి రీసెట్ అవుతుంది.\nఅపరిమిత వినియోగానికి /subscribe చేయండి.",
        "quota_left": "📊 ఈరోజు {remaining} ఉచిత వినియోగాలు మిగిలాయి. {reset} లో 12:00 AM ISTకి రీసెట్ అవుతుంది.",
        "folder_premium": "📁 ఫోల్డర్ డౌన్‌లోడ్ ప్రీమియం ఫీచర్.\n\nఫోల్డర్, అపరిమిత డౌన్‌లోడ్‌లు, /random మరియు /search కోసం /subscribe చేయండి.",
    },
    "kn": {
        "welcome_plans": "🆓 ಉಚಿತ ಮಿತಿ: ದಿನಕ್ಕೆ 10 ಡೌನ್‌ಲೋಡ್‌ಗಳು, 10 /random ಮತ್ತು 10 /search. ಫೋಲ್ಡರ್ ಡೌನ್‌ಲೋಡ್‌ಗಳು ಪ್ರೀಮಿಯಂ.\n⭐ ಅಪರಿಮಿತ ಬಳಕೆಗೆ /subscribe ಮಾಡಿ.",
        "limit_terabox": "⏳ ದೈನಂದಿನ ಮಿತಿ ಮುಗಿದಿದೆ — ದಿನಕ್ಕೆ {limit} TeraBox ಫೈಲ್‌ಗಳು.\n\n{reset} ನಲ್ಲಿ 12:00 AM ISTಕ್ಕೆ ಮರುಹೊಂದಿಸಲಾಗುತ್ತದೆ.\nಅಪರಿಮಿತ ಡೌನ್‌ಲೋಡ್‌ಗಳಿಗೆ /subscribe ಮಾಡಿ.",
        "limit_random": "⏳ ದೈನಂದಿನ ಮಿತಿ ಮುಗಿದಿದೆ — ದಿನಕ್ಕೆ {limit} /random ಬಳಕೆಗಳು.\n\n{reset} ನಲ್ಲಿ 12:00 AM ISTಕ್ಕೆ ಮರುಹೊಂದಿಸಲಾಗುತ್ತದೆ.\nಅಪರಿಮಿತ ಬಳಕೆಗೆ /subscribe ಮಾಡಿ.",
        "limit_search": "⏳ ದೈನಂದಿನ ಮಿತಿ ಮುಗಿದಿದೆ — ದಿನಕ್ಕೆ {limit} /search ಬಳಕೆಗಳು.\n\n{reset} ನಲ್ಲಿ 12:00 AM ISTಕ್ಕೆ ಮರುಹೊಂದಿಸಲಾಗುತ್ತದೆ.\nಅಪರಿಮಿತ ಬಳಕೆಗೆ /subscribe ಮಾಡಿ.",
        "quota_left": "📊 ಇಂದು {remaining} ಉಚಿತ ಬಳಕೆಗಳು ಉಳಿದಿವೆ. {reset} ನಲ್ಲಿ 12:00 AM ISTಕ್ಕೆ ಮರುಹೊಂದಿಸಲಾಗುತ್ತದೆ.",
        "folder_premium": "📁 ಫೋಲ್ಡರ್ ಡೌನ್‌ಲೋಡ್ ಪ್ರೀಮಿಯಂ ವೈಶಿಷ್ಟ್ಯ.\n\nಫೋಲ್ಡರ್, ಅಪರಿಮಿತ ಡೌನ್‌ಲೋಡ್‌ಗಳು, /random ಮತ್ತು /search ಗಾಗಿ /subscribe ಮಾಡಿ.",
    },
    "ml": {
        "welcome_plans": "🆓 സൗജന്യ പരിധി: ദിവസം 10 ഡൗൺലോഡുകൾ, 10 /random, 10 /search. ഫോൾഡർ ഡൗൺലോഡുകൾ പ്രീമിയമാണ്.\n⭐ പരിധിയില്ലാത്ത ഉപയോഗത്തിന് /subscribe ചെയ്യുക.",
        "limit_terabox": "⏳ ദൈനംദിന പരിധി തീർന്നു — ദിവസം {limit} TeraBox ഫയലുകൾ.\n\n{reset} കഴിഞ്ഞ് 12:00 AM IST-ന് പുനഃസജ്ജമാകും.\nപരിധിയില്ലാത്ത ഡൗൺലോഡുകൾക്ക് /subscribe ചെയ്യുക.",
        "limit_random": "⏳ ദൈനംദിന പരിധി തീർന്നു — ദിവസം {limit} /random ഉപയോഗങ്ങൾ.\n\n{reset} കഴിഞ്ഞ് 12:00 AM IST-ന് പുനഃസജ്ജമാകും.\nപരിധിയില്ലാത്ത ഉപയോഗത്തിന് /subscribe ചെയ്യുക.",
        "limit_search": "⏳ ദൈനംദിന പരിധി തീർന്നു — ദിവസം {limit} /search ഉപയോഗങ്ങൾ.\n\n{reset} കഴിഞ്ഞ് 12:00 AM IST-ന് പുനഃസജ്ജമാകും.\nപരിധിയില്ലാത്ത ഉപയോഗത്തിന് /subscribe ചെയ്യുക.",
        "quota_left": "📊 ഇന്ന് {remaining} സൗജന്യ ഉപയോഗങ്ങൾ ബാക്കി. {reset} കഴിഞ്ഞ് 12:00 AM IST-ന് പുനഃസജ്ജമാകും.",
        "folder_premium": "📁 ഫോൾഡർ ഡൗൺലോഡ് ഒരു പ്രീമിയം സവിശേഷതയാണ്.\n\nഫോൾഡർ, പരിധിയില്ലാത്ത ഡൗൺലോഡുകൾ, /random, /search എന്നിവയ്ക്ക് /subscribe ചെയ്യുക.",
    },
    "ur": {
        "welcome_plans": "🆓 مفت حد: روزانہ 10 ڈاؤن لوڈز، 10 /random اور 10 /search۔ فولڈر ڈاؤن لوڈز پریمیم ہیں۔\n⭐ لامحدود استعمال کے لیے /subscribe کریں۔",
        "limit_terabox": "⏳ روزانہ کی حد پوری — روزانہ {limit} TeraBox فائلیں۔\n\n{reset} میں 12:00 AM IST پر ری سیٹ ہوگی۔\nلامحدود ڈاؤن لوڈز کے لیے /subscribe کریں۔",
        "limit_random": "⏳ روزانہ کی حد پوری — روزانہ {limit} /random استعمال۔\n\n{reset} میں 12:00 AM IST پر ری سیٹ ہوگی۔\nلامحدود استعمال کے لیے /subscribe کریں۔",
        "limit_search": "⏳ روزانہ کی حد پوری — روزانہ {limit} /search استعمال۔\n\n{reset} میں 12:00 AM IST پر ری سیٹ ہوگی۔\nلامحدود استعمال کے لیے /subscribe کریں۔",
        "quota_left": "📊 آج {remaining} مفت استعمال باقی ہیں۔ {reset} میں 12:00 AM IST پر ری سیٹ ہوں گے۔",
        "folder_premium": "📁 فولڈر ڈاؤن لوڈ ایک پریمیم فیچر ہے۔\n\nفولڈر، لامحدود ڈاؤن لوڈز، /random اور /search کے لیے /subscribe کریں۔",
    },
    "pa": {
        "welcome_plans": "🆓 ਮੁਫ਼ਤ ਸੀਮਾ: ਰੋਜ਼ਾਨਾ 10 ਡਾਊਨਲੋਡ, 10 /random ਅਤੇ 10 /search। ਫੋਲਡਰ ਡਾਊਨਲੋਡ ਪ੍ਰੀਮੀਅਮ ਹਨ।\n⭐ ਅਸੀਮਤ ਵਰਤੋਂ ਲਈ /subscribe ਕਰੋ।",
        "limit_terabox": "⏳ ਰੋਜ਼ਾਨਾ ਸੀਮਾ ਪੂਰੀ — ਰੋਜ਼ਾਨਾ {limit} TeraBox ਫਾਈਲਾਂ।\n\n{reset} ਵਿੱਚ 12:00 AM IST 'ਤੇ ਰੀਸੈਟ ਹੋਵੇਗੀ।\nਅਸੀਮਤ ਡਾਊਨਲੋਡ ਲਈ /subscribe ਕਰੋ।",
        "limit_random": "⏳ ਰੋਜ਼ਾਨਾ ਸੀਮਾ ਪੂਰੀ — ਰੋਜ਼ਾਨਾ {limit} /random ਵਰਤੋਂ।\n\n{reset} ਵਿੱਚ 12:00 AM IST 'ਤੇ ਰੀਸੈਟ ਹੋਵੇਗੀ।\nਅਸੀਮਤ ਵਰਤੋਂ ਲਈ /subscribe ਕਰੋ।",
        "limit_search": "⏳ ਰੋਜ਼ਾਨਾ ਸੀਮਾ ਪੂਰੀ — ਰੋਜ਼ਾਨਾ {limit} /search ਵਰਤੋਂ।\n\n{reset} ਵਿੱਚ 12:00 AM IST 'ਤੇ ਰੀਸੈਟ ਹੋਵੇਗੀ।\nਅਸੀਮਤ ਵਰਤੋਂ ਲਈ /subscribe ਕਰੋ।",
        "quota_left": "📊 ਅੱਜ {remaining} ਮੁਫ਼ਤ ਵਰਤੋਂ ਬਾਕੀ। {reset} ਵਿੱਚ 12:00 AM IST 'ਤੇ ਰੀਸੈਟ ਹੋਵੇਗੀ।",
        "folder_premium": "📁 ਫੋਲਡਰ ਡਾਊਨਲੋਡ ਇੱਕ ਪ੍ਰੀਮੀਅਮ ਸੁਵਿਧਾ ਹੈ।\n\nਫੋਲਡਰ, ਅਸੀਮਤ ਡਾਊਨਲੋਡ, /random ਅਤੇ /search ਲਈ /subscribe ਕਰੋ।",
    },
    "gu": {
        "welcome_plans": "🆓 મફત મર્યાદા: દરરોજ 10 ડાઉનલોડ, 10 /random અને 10 /search. ફોલ્ડર ડાઉનલોડ પ્રીમિયમ છે.\n⭐ અમર્યાદિત વપરાશ માટે /subscribe કરો.",
        "limit_terabox": "⏳ દૈનિક મર્યાદા પૂર્ણ — દરરોજ {limit} TeraBox ફાઇલો.\n\n{reset} માં 12:00 AM IST પર રીસેટ થશે.\nઅમર્યાદિત ડાઉનલોડ માટે /subscribe કરો.",
        "limit_random": "⏳ દૈનિક મર્યાદા પૂર્ણ — દરરોજ {limit} /random વપરાશ.\n\n{reset} માં 12:00 AM IST પર રીસેટ થશે.\nઅમર્યાદિત વપરાશ માટે /subscribe કરો.",
        "limit_search": "⏳ દૈનિક મર્યાદા પૂર્ણ — દરરોજ {limit} /search વપરાશ.\n\n{reset} માં 12:00 AM IST પર રીસેટ થશે.\nઅમર્યાદિત વપરાશ માટે /subscribe કરો.",
        "quota_left": "📊 આજે {remaining} મફત વપરાશ બાકી. {reset} માં 12:00 AM IST પર રીસેટ થશે.",
        "folder_premium": "📁 ફોલ્ડર ડાઉનલોડ એ પ્રીમિયમ સુવિધા છે.\n\nફોલ્ડર, અમર્યાદિત ડાઉનલોડ, /random અને /search માટે /subscribe કરો.",
    },
    "es": {
        "welcome_plans": "🆓 Plan gratis: 10 descargas, 10 /random y 10 /search al día. Las descargas de carpetas son premium.\n⭐ Usa /subscribe para acceso ilimitado.",
        "limit_terabox": "⏳ Límite diario alcanzado — {limit} archivos de TeraBox al día.\n\nSe reinicia en {reset} a las 12:00 AM IST.\nUsa /subscribe para descargas ilimitadas.",
        "limit_random": "⏳ Límite diario alcanzado — {limit} usos de /random al día.\n\nSe reinicia en {reset} a las 12:00 AM IST.\nUsa /subscribe para uso ilimitado.",
        "limit_search": "⏳ Límite diario alcanzado — {limit} usos de /search al día.\n\nSe reinicia en {reset} a las 12:00 AM IST.\nUsa /subscribe para uso ilimitado.",
        "quota_left": "📊 Te quedan {remaining} usos gratis hoy. Se reinicia en {reset} a las 12:00 AM IST.",
        "folder_premium": "📁 Las descargas de carpetas son una función premium.\n\nUsa /subscribe para desbloquear carpetas, descargas ilimitadas, /random y /search.",
    },
    "fr": {
        "welcome_plans": "🆓 Offre gratuite : 10 téléchargements, 10 /random et 10 /search par jour. Les dossiers sont premium.\n⭐ Utilisez /subscribe pour un accès illimité.",
        "limit_terabox": "⏳ Limite quotidienne atteinte — {limit} fichiers TeraBox par jour.\n\nRéinitialisation dans {reset} à 12:00 AM IST.\nUtilisez /subscribe pour des téléchargements illimités.",
        "limit_random": "⏳ Limite quotidienne atteinte — {limit} utilisations de /random par jour.\n\nRéinitialisation dans {reset} à 12:00 AM IST.\nUtilisez /subscribe pour un usage illimité.",
        "limit_search": "⏳ Limite quotidienne atteinte — {limit} utilisations de /search par jour.\n\nRéinitialisation dans {reset} à 12:00 AM IST.\nUtilisez /subscribe pour un usage illimité.",
        "quota_left": "📊 Il vous reste {remaining} utilisations gratuites aujourd'hui. Réinitialisation dans {reset} à 12:00 AM IST.",
        "folder_premium": "📁 Les téléchargements de dossiers sont une fonction premium.\n\nUtilisez /subscribe pour débloquer les dossiers, les téléchargements illimités, /random et /search.",
    },
    "de": {
        "welcome_plans": "🆓 Kostenlos: 10 Downloads, 10 /random und 10 /search pro Tag. Ordner-Downloads sind Premium.\n⭐ Nutze /subscribe für unbegrenzten Zugriff.",
        "limit_terabox": "⏳ Tageslimit erreicht — {limit} TeraBox-Dateien pro Tag.\n\nZurücksetzung in {reset} um 12:00 AM IST.\nNutze /subscribe für unbegrenzte Downloads.",
        "limit_random": "⏳ Tageslimit erreicht — {limit} /random-Nutzungen pro Tag.\n\nZurücksetzung in {reset} um 12:00 AM IST.\nNutze /subscribe für unbegrenzte Nutzung.",
        "limit_search": "⏳ Tageslimit erreicht — {limit} /search-Nutzungen pro Tag.\n\nZurücksetzung in {reset} um 12:00 AM IST.\nNutze /subscribe für unbegrenzte Nutzung.",
        "quota_left": "📊 Heute noch {remaining} kostenlose Nutzungen. Zurücksetzung in {reset} um 12:00 AM IST.",
        "folder_premium": "📁 Ordner-Downloads sind eine Premium-Funktion.\n\nNutze /subscribe für Ordner, unbegrenzte Downloads, /random und /search.",
    },
    "it": {
        "welcome_plans": "🆓 Piano gratuito: 10 download, 10 /random e 10 /search al giorno. I download delle cartelle sono premium.\n⭐ Usa /subscribe per accesso illimitato.",
        "limit_terabox": "⏳ Limite giornaliero raggiunto — {limit} file TeraBox al giorno.\n\nSi azzera tra {reset} alle 12:00 AM IST.\nUsa /subscribe per download illimitati.",
        "limit_random": "⏳ Limite giornaliero raggiunto — {limit} utilizzi di /random al giorno.\n\nSi azzera tra {reset} alle 12:00 AM IST.\nUsa /subscribe per utilizzo illimitato.",
        "limit_search": "⏳ Limite giornaliero raggiunto — {limit} utilizzi di /search al giorno.\n\nSi azzera tra {reset} alle 12:00 AM IST.\nUsa /subscribe per utilizzo illimitato.",
        "quota_left": "📊 Oggi ti restano {remaining} utilizzi gratuiti. Si azzera tra {reset} alle 12:00 AM IST.",
        "folder_premium": "📁 I download delle cartelle sono una funzione premium.\n\nUsa /subscribe per sbloccare cartelle, download illimitati, /random e /search.",
    },
    "ja": {
        "welcome_plans": "🆓 無料プラン：1日10回のダウンロード、10回の/random、10回の/search。フォルダーのダウンロードはプレミアムです。\n⭐ 無制限にするには /subscribe を使ってください。",
        "limit_terabox": "⏳ 1日の上限に達しました — 1日{limit}件のTeraBoxファイル。\n\n{reset}後に12:00 AM ISTにリセットされます。\n無制限のダウンロードには /subscribe を使ってください。",
        "limit_random": "⏳ 1日の上限に達しました — 1日{limit}回の/random。\n\n{reset}後に12:00 AM ISTにリセットされます。\n無制限の利用には /subscribe を使ってください。",
        "limit_search": "⏳ 1日の上限に達しました — 1日{limit}回の/search。\n\n{reset}後に12:00 AM ISTにリセットされます。\n無制限の利用には /subscribe を使ってください。",
        "quota_left": "📊 今日は残り{remaining}回無料で利用できます。{reset}後に12:00 AM ISTにリセットされます。",
        "folder_premium": "📁 フォルダーのダウンロードはプレミアム機能です。\n\nフォルダー、無制限のダウンロード、/random、/searchを利用するには /subscribe を使ってください。",
    },
    "ko": {
        "welcome_plans": "🆓 무료 요금제: 하루 10회 다운로드, 10회 /random, 10회 /search. 폴더 다운로드는 프리미엄입니다.\n⭐ 무제한 이용은 /subscribe를 사용하세요.",
        "limit_terabox": "⏳ 일일 한도에 도달했습니다 — 하루 {limit}개의 TeraBox 파일.\n\n{reset} 후 12:00 AM IST에 초기화됩니다.\n무제한 다운로드는 /subscribe를 사용하세요.",
        "limit_random": "⏳ 일일 한도에 도달했습니다 — 하루 {limit}회의 /random.\n\n{reset} 후 12:00 AM IST에 초기화됩니다.\n무제한 이용은 /subscribe를 사용하세요.",
        "limit_search": "⏳ 일일 한도에 도달했습니다 — 하루 {limit}회의 /search.\n\n{reset} 후 12:00 AM IST에 초기화됩니다.\n무제한 이용은 /subscribe를 사용하세요.",
        "quota_left": "📊 오늘 무료 이용 {remaining}회 남았습니다. {reset} 후 12:00 AM IST에 초기화됩니다.",
        "folder_premium": "📁 폴더 다운로드는 프리미엄 기능입니다.\n\n폴더, 무제한 다운로드, /random, /search를 이용하려면 /subscribe를 사용하세요.",
    },
    "zh": {
        "welcome_plans": "🆓 免费额度：每天 10 次下载、10 次 /random 和 10 次 /search。文件夹下载为高级功能。\n⭐ 使用 /subscribe 解锁无限使用。",
        "limit_terabox": "⏳ 已达每日上限 — 每天 {limit} 个 TeraBox 文件。\n\n将在 {reset} 后于 IST 凌晨 12:00 重置。\n使用 /subscribe 解锁无限下载。",
        "limit_random": "⏳ 已达每日上限 — 每天 {limit} 次 /random。\n\n将在 {reset} 后于 IST 凌晨 12:00 重置。\n使用 /subscribe 解锁无限使用。",
        "limit_search": "⏳ 已达每日上限 — 每天 {limit} 次 /search。\n\n将在 {reset} 后于 IST 凌晨 12:00 重置。\n使用 /subscribe 解锁无限使用。",
        "quota_left": "📊 今天还剩 {remaining} 次免费使用。将在 {reset} 后于 IST 凌晨 12:00 重置。",
        "folder_premium": "📁 文件夹下载是高级功能。\n\n使用 /subscribe 解锁文件夹、无限下载、/random 和 /search。",
    },
}

for _code, _extra in PREMIUM_TRANSLATIONS.items():
    TRANSLATIONS.setdefault(_code, {}).update(_extra)




