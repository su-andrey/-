
import pygame as pg
import pygame.freetype as freetype


PRINT_EVENT = False
CHATLIST_POS = pg.Rect(0, 20, 1150, 400)
CHATBOX_POS = pg.Rect(0, 350, 1150, 40)


pg.init()

FPSClock = pg.time.Clock()
Screen = pg.display.set_mode((600, 500))
Font = freetype.SysFont('arial', 24)


def main():

    global BGCOLOR, PRINT_EVENT, CHATBOX_POS, CHATLIST_POS, CHATLIST_MAXSIZE
    global FPSClock, Font, Screen
    pg.key.start_text_input()
    input_rect = pg.Rect(80, 80, 320, 40)
    pg.key.set_text_input_rect(input_rect)

    _IMEEditing = False
    _IMEText = ""
    _IMETextPos = 0
    _IMEEditingText = ""
    _IMEEditingPos = 0
    ChatList = []
    tex = 1
    while tex:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if _IMEEditing:
                    if len(_IMEEditingText) == 0:
                        _IMEEditing = False
                    continue
                if event.key == pg.K_BACKSPACE:
                    if len(_IMEText) > 0 and _IMETextPos > 0:
                        _IMEText = (
                                _IMEText[0: _IMETextPos - 1] + _IMEText[_IMETextPos:]
                        )
                        _IMETextPos = max(0, _IMETextPos - 1)
                elif event.key == pg.K_DELETE:
                    _IMEText = _IMEText[0:_IMETextPos] + _IMEText[_IMETextPos + 1:]
                elif event.key == pg.K_LEFT:
                    _IMETextPos = max(0, _IMETextPos - 1)
                elif event.key == pg.K_RIGHT:
                    _IMETextPos = min(len(_IMEText), _IMETextPos + 1)
                elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                    if len(_IMEText) == 0:
                        continue
                    # Append chat list
                    ChatList.append(_IMEText)
                    pg.display.flip()
                    return _IMEText
            elif event.type == pg.TEXTEDITING:
                if PRINT_EVENT:
                    print(event)
                _IMEEditing = True
                _IMEEditingText = event.text
                _IMEEditingPos = event.start

            elif event.type == pg.TEXTINPUT:
                if PRINT_EVENT:
                    print(event)
                _IMEEditing = False
                _IMEEditingText = ""
                _IMEText = _IMEText[0:_IMETextPos] + event.text + _IMEText[_IMETextPos:]
                _IMETextPos += len(event.text)
        Screen.fill('sandybrown')


        start_pos = CHATBOX_POS.copy()
        ime_textL = "|" + _IMEText[0:_IMETextPos]
        ime_textM = (
                _IMEEditingText[0:_IMEEditingPos] + "|" + _IMEEditingText[_IMEEditingPos:]
        )
        ime_textR = _IMEText[_IMETextPos:]

        rect_textL = Font.render_to(Screen, start_pos, ime_textL, 'dimgray')
        start_pos.x += rect_textL.width

        # Editing texts should be underlined
        rect_textM = Font.render_to(
            Screen, start_pos, ime_textM, 'green', None, freetype.STYLE_UNDERLINE
        )
        start_pos.x += rect_textM.width
        Font.render_to(Screen, start_pos, ime_textR, 'green')
        pg.display.update()




