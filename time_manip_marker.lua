---- time_manip_marker.lua
-- time stretching markers
-- ie markers at t = 14 32 56 with a factor of .5
-- will be moved to t = 7 16 28
ardour {
	["type"] = "EditorAction",
	name = "Change Speed of Markers",
    author = "Flarp",
    license = "BSD",
    description = "Move markers by transforming them with a given factor",
}

function factory (_nada)
	return function()
		local v = Session:locations():list()
        local dialog_contents = {
            { type = "heading", title = "Change Marker Speed" },
            { type = "number", key = "factor", title = "Stretch factor", min = 0, max = 1000, step = 0.001, digits = 20, default = 1 },
        }
        local dialog_gui = LuaDialog.Dialog("Change Marker Speed", dialog_contents)
        local results = dialog_gui:run()
		for location in v:iter() do
			if location:is_mark() then
				location:move_to(math.floor(location:start() * results["factor"]), 0)
			end
		end
	end
end
