local logger = {}
local mod = logger

function mod.log(str, color)
    return function(...)
        print(string.format("%s%s\x1b[0m", color, str), ...)
    end
end
-- blue
mod.DEBUG = mod.log("[DEBUG]", "\x1b[34m")
-- green
mod.INFO = mod.log("[INFO]", "\x1b[32m")
-- white
mod.WARN = mod.log("[WARE]", "\x1b[33m")
-- red
mod.ERROR = mod.log("[ERROR]", "\x1b[31m")

return logger

