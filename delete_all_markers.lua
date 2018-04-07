ardour {
	["type"] = "EditorAction",
	name = "Remove All Markers",
	author = "Flarp",
	license = "BSD",
	description = "Deletes all markers in the current session."
}
function factory(_nada)
	return function()
		local locations = Session:locations()
		for location in locations:list():iter() do
			if location:is_mark() then
				locations:remove(location)
			end
		end
	end
end