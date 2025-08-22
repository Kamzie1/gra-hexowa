from projekt.assetMenager import AssetManager


class AnimationMenager:
    animations = []  # (time, type, content, pos)

    @staticmethod
    def display(screen):
        for animation in AnimationMenager.animations:
            AnimationMenager.draw(animation, screen)

    @staticmethod
    def update():
        AnimationMenager.animations = [
            (animation[0] - 1, animation[1], animation[2], animation[3])
            for animation in AnimationMenager.animations
            if animation[0] > 0
        ]

    @staticmethod
    def draw(animation, screen):
        match (animation[1]):
            case 0:
                AnimationMenager.draw_text(animation, screen)

    @staticmethod
    def draw_text(animation, screen):
        text = AssetManager.get_font("consolas", 26).render(animation[2], True, "red")
        if animation[0] < 4:
            text.set_alpha(240)
        if animation[0] > 36:
            text.set_alpha(240)
        if animation[0] < 12:
            text.set_alpha(200)
        if animation[0] > 28:
            text.set_alpha(200)
        text_rect = text.get_frect(center=animation[3])
        screen.blit(text, text_rect)
