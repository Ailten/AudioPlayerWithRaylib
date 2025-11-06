import pyray # python3 -m pip install raylib==5.5.0.3
import asyncio
from script.function import * 
import pathlib


# ----------> Main function.

async def main():

    #TODO: 
    # switch to draw_text_pro and eval_size for make it clamp in the box.

    # main path.
    pathMain = pathlib.Path(__file__).parent.resolve()

    # build a window.
    param = getJsonObj(pathMain)

    # get list path of mp3.
    musicsNameFiles = getAllFilesName(param["musicFolderPath"])
    musicIndex = 0

    # init window.
    pyray.init_window(param["windowSize"][0], param["windowSize"][1], "AudioPlayer_Ailt")
    backgroundColor = pyray.Color(
        param["backgroundColor"][0], 
        param["backgroundColor"][1], 
        param["backgroundColor"][2], 
        param["backgroundColor"][3]
    )
    pyray.set_target_fps(param["fps"])
    pyray.init_audio_device()

    # textures.
    backgroundTexture = pyray.load_texture(f"{pathMain}/spryte/_background.png")
    defaultMusicTexture = pyray.load_texture(f"{pathMain}/spryte/_unknowMusic.png")
    currentMusicTexture = None
    defaultOrigine = pyray.Vector2(0, 0)
    backgroundSource = pyray.Rectangle(0, 0, param["windowSize"][0], param["windowSize"][1])
    illuSource = pyray.Rectangle(0, 0, param["sizeIllu"][0], param["sizeIllu"][0])
    illuDest = pyray.Rectangle(param["posIllu"][0], param["posIllu"][1], param["sizeIllu"][0], param["sizeIllu"][1])

    # music.
    music = pyray.load_music_stream(f"{param['musicFolderPath']}/{musicsNameFiles[musicIndex]}.mp3")
    pyray.play_music_stream(music)
    musicLength = pyray.get_music_time_length(music)
    currentTimePlayed = 0
    lastTimePlayed = 0
    pyray.set_music_volume(music, param['volume'])

    # sprite music.
    potentialPathMusicTexture = f"{pathMain}/spryte/{musicsNameFiles[musicIndex]}.png"
    currentMusicTexture = pyray.load_texture(potentialPathMusicTexture) if isHasMusicTexture(potentialPathMusicTexture) else None

    # font.
    font = pyray.load_font_ex(f"{pathMain}/font/{param['font']}.ttf", param["sizeName"][1], None, 0)
    posName = pyray.Vector2(param["posName"][0], param["posName"][1])
    textColor = pyray.Color(
        param["textColor"][0], 
        param["textColor"][1], 
        param["textColor"][2], 
        param["textColor"][3]
    )

    # loop update.
    while not pyray.window_should_close():

        # update music played.
        pyray.update_music_stream(music)

        # is music play is end.
        currentTimePlayed = pyray.get_music_time_played(music)
        if currentTimePlayed < lastTimePlayed:

            # load and play the next music.
            pyray.unload_music_stream(music)
            musicIndex = (musicIndex + 1) % len(musicsNameFiles)
            music = pyray.load_music_stream(f"{param['musicFolderPath']}/{musicsNameFiles[musicIndex]}.mp3")
            pyray.play_music_stream(music)
            musicLength = pyray.get_music_time_length(music)
            currentTimePlayed = 0
            pyray.set_music_volume(music, param['volume'])

            # load illu.
            if currentMusicTexture is not None:
                pyray.unload_texture(currentMusicTexture)
            potentialPathMusicTexture = f"{pathMain}/spryte/{musicsNameFiles[musicIndex]}.png"
            currentMusicTexture = pyray.load_texture(potentialPathMusicTexture) if isHasMusicTexture(potentialPathMusicTexture) else None

        lastTimePlayed = currentTimePlayed

        # draw phase start. ------>
        pyray.begin_drawing()
        pyray.clear_background(backgroundColor)

        # draw background illu.
        pyray.draw_texture_pro(
            backgroundTexture,
            backgroundSource,
            backgroundSource, # Dest.
            defaultOrigine,
            0,
            pyray.WHITE
        )

        # draw illu.
        pyray.draw_texture_pro(
            currentMusicTexture or defaultMusicTexture,
            illuSource,
            illuDest,
            defaultOrigine,
            0,
            pyray.WHITE
        )

        # draw name.
        pyray.draw_text_ex(
            font,
            musicsNameFiles[musicIndex],
            posName,
            float(font.baseSize),
            0,
            textColor
        )

        # draw phase end. ------>
        pyray.end_drawing()

    # free textures and music.
    pyray.unload_texture(backgroundTexture)
    pyray.unload_texture(defaultMusicTexture)
    pyray.unload_music_stream(music)
    if currentMusicTexture is not None:
        pyray.unload_texture(currentMusicTexture)
    pyray.unload_font(font)

    # close window.
    pyray.close_audio_device()
    pyray.close_window()

# ---------->

# call main.
asyncio.run(main())