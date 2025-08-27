from projekt.assetMenager import AssetManager


class AnimationMenager:
    animations = []  # (time, type, content, pos)

    @staticmethod
    def display(screen):
        i = 0
        for animation in AnimationMenager.animations:
            AnimationMenager.draw(animation, screen, i)
            i += 1

    @staticmethod
    def update():
        AnimationMenager.animations = [
            (animation[0] - 1, animation[1], animation[2], animation[3])
            for animation in AnimationMenager.animations
            if animation[0] > 0
        ]

    @staticmethod
    def draw(animation, screen, i):
        match (animation[1]):
            case 0:
                AnimationMenager.draw_text(animation, screen, i)

    @staticmethod
    def draw_text(animation, screen, i):
        for j in range(i):
            if AnimationMenager.animations[j][1] == animation[1]:
                AnimationMenager.animations[i] = (
                    animation[0] + 1,
                    animation[1],
                    animation[2],
                    animation[3],
                )
                return
        text = AssetManager.get_font("consolas", 26).render(animation[2], True, "red")
        if animation[0] < 24:
            text.set_alpha(240)
        if animation[0] > 54:
            text.set_alpha(240)
        if animation[0] < 32:
            text.set_alpha(200)
        if animation[0] > 48:
            text.set_alpha(200)
        if animation[0] > 20:
            text_rect = text.get_frect(center=animation[3])
            screen.blit(text, text_rect)
