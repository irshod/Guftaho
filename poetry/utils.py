"""
Utility functions for Persian to Tajik Cyrillic text conversion
"""

# Persian to Tajik Cyrillic mapping dictionary
PERSIAN_TO_TAJIK_MAPPING = {
    # Common Persian words to Tajik Cyrillic
    'گفتگو': 'Гуфтугў',
    'کتابخانه': 'Китобхона',
    'کتابخانۀ': 'Китобхона',
    'شعر': 'Шеър',
    'تاجیک': 'Тоҷик',
    'شاعران': 'Шоирон',
    'شاعر': 'Шоир',
    'کتاب': 'Китоб',
    'کتابها': 'Китобҳо',
    'شعرها': 'Шеърҳо',
    'نام': 'Ном',
    'خانه': 'Хона',
    'جستجو': 'Ҷустуҷў',
    'مشاهده': 'Мушоҳида',
    'آثار': 'Осор',
    'اطلاعات': 'Маълумот',
    'اصلی': 'Асосӣ',
    'زندگی': 'Зиндагӣ',
    'توضیحات': 'Шарҳ',
    'متن': 'Матн',
    'تاریخ': 'Таърих',
    'نشر': 'Нашр',
    'متولد': 'Таваллуд',
    'فوت': 'Вафот',
    'سال': 'Сол',
    'صفحه': 'Саҳифа',
    'بندی': 'Банди',
    'نتایج': 'natijlar',
    'برای': 'барои',
    'پاک': 'поку',
    'کردن': 'кунание',
    'مجموعه': 'Маҷмуа',
    'جامع': 'Ҷомеъ',
    'از': 'аз',
    'نامدار': 'номдор',
    'ساخته': 'сохта',
    'شده': 'шуда',
    'با': 'бо',
    'برای': 'барои',
    'حفظ': 'ҳифз',
    'و': 'ва',
    'فرهنگ': 'Фарҳанг',
    
    # Rudaki specific
    'ابوعبدالله': 'Абуабдуллоҳ',
    'جعفر': 'Ҷаъфар',
    'رودکی': 'Рудакӣ',
    'پدر': 'падар',
    'فارسی': 'Форсӣ',
    'محسوب': 'маҳсуб',
    'میشود': 'мешавад',
    'او': 'ў',
    'اولین': 'аввалин',
    'است': 'аст',
    'میلادی': 'милодӣ',
    'بزرگ': 'бузург',
    'شاعری': 'шоире',
    'که': 'ки',
    
    # Numbers
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', 
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
    
    # Common date/time words
    'هیچ': 'ҳеч',
    'هنوز': 'ҳанӯз',
    'اضافه': 'илова',
    'نشده': 'нашуда',
    'یافت': 'ёфт',
    'این': 'ин',
    'برای': 'барои',
    'پیش': 'пеш',
    'بعد': 'баъд',
    'بعدی': 'баъдӣ',
}

def convert_persian_to_tajik(text):
    """
    Convert Persian text to Tajik Cyrillic
    
    Args:
        text (str): Persian text to convert
        
    Returns:
        str: Converted Tajik Cyrillic text
    """
    if not text:
        return text
        
    # Convert the text using the mapping dictionary
    converted_text = text
    for persian, tajik in PERSIAN_TO_TAJIK_MAPPING.items():
        converted_text = converted_text.replace(persian, tajik)
    
    return converted_text

def get_tajik_translations():
    """
    Get common Tajik translations for UI elements
    
    Returns:
        dict: Dictionary of translated UI elements
    """
    return {
        # Navigation
        'home': 'Асосӣ',
        'search': 'Ҷустуҷў',
        'quick_search': 'Ҷустуҷўи тез...',
        
        # Page titles
        'poets': 'Шоирон',
        'poet': 'Шоир',
        'book': 'Китоб',
        'books': 'Китобҳо',
        'poem': 'Шеър',
        'poems': 'Шеърҳо',
        'works': 'Осор',
        
        # Actions
        'view_works': 'Осорро дидан',
        'view_poems': 'Шеърҳоро дидан',
        'copy': 'Нусха кардан',
        'previous_poem': 'Шеъри пешин',
        'next_poem': 'Шеъри оянда',
        
        # Info
        'born': 'Таваллуд',
        'died': 'Вафот',
        'publication_date': 'Санаи нашр',
        'no_poets_found': 'Ҳеч шоире ёфт нашуд',
        'no_poets_added': 'Ҳанӯз ҳеч шоире илова нашудааст',
        'search_results_for': 'Натиҷаҳои ҷустуҷў барои',
        'clear_search': 'Ҷустуҷўро пок кунед',
        
        # Footer
        'library_subtitle': 'Маҷмӯаи ҷомеи осори шоирони номдори тоҷик',
        'made_with_love': 'бо ❤️ барои ҳифзу ташри фарҳанги тоҷик сохта шуд',
        
        # Site title
        'site_title': 'Гуфтугў',
        'site_subtitle': 'Китобхонаи шеъри тоҷик',
    }