import vedro

import vedro_jj
import vedro_pw


class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):
        class Playwright(vedro_pw.Playwright):
            enabled = True

        class VedroJJ(vedro_jj.VedroJJ):
            enabled = True
            host = "localhost"
            port = 8080
