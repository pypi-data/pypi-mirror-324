from aiogram.utils.keyboard import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardButton, KeyboardBuilder

def get_builder():
    return KeyboardBuilder(
        button_type=InlineKeyboardButton
    )
    

async def create_yes_no_markup(keyword):
    
    builder = get_builder()
    
    builder.add(
        InlineKeyboardButton(text="Yes", callback_data= f"{keyword}:yes")
    )
    builder.add(
        InlineKeyboardButton(text="No", callback_data= f"{keyword}:no")
    )
    return builder.as_markup()


async def mass_button_markup(buttons, page: int, buttons_per_page: int, row_width: int = 2):
    start_index = (page - 1) * buttons_per_page
    end_index = start_index + buttons_per_page

    keyboard =get_builder()
    keyboard.adjust(row_width)
    
    for i in range(start_index, end_index, row_width):
        keyboard.add(*buttons[i:i + 2])
    return keyboard.as_markup()


def add_navigation_button_markup(current_page: int, total_pages: int, identifier: str, deliver_buttons=False):
    buttons = []
    keyboard = get_builder()
    if current_page > 1:
        buttons.append(
            InlineKeyboardButton(text="See Previous", callback_data=f"{identifier}:{current_page-1}")
        )
    if current_page < total_pages:
        buttons.append(
            InlineKeyboardButton(text="See Next", callback_data=f"{identifier}:{current_page+1}")
        )
    if deliver_buttons:
        return buttons

    keyboard.add(*buttons)
    return keyboard.as_markup()

async def dynamic_dictionary_markup(buttons, row_width=1, deliver_buttons=False):
    keyboard = get_builder()
    
    button_list = []
    for text, callback_data in buttons.items():
        button = InlineKeyboardButton(text=text, callback_data=callback_data)
        keyboard.add(button)
        button_list.append(button)

    keyboard.adjust(row_width)
    if not deliver_buttons:
        return keyboard.as_markup()
    else:
        return button_list

async def gen_link_markup(buttons, row_width=1, deliver_buttons=False):
    keyboard = get_builder()
    
    button_list = []
    for text, url in buttons.items():
        button = InlineKeyboardButton(text=text, url=url)
        keyboard.add(button)
        button_list.append(button)

    if not deliver_buttons:
        keyboard.adjust(row_width)
        return keyboard.as_markup()
    else:
        return button_list
    