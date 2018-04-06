ardour {
    ["type"] = "EditorAction",
    name = "Export Markers to MIDI Notes",
    author = "Flarp",
    license = "BSD",
    description = "Export every marker to a single note in a MIDI file",
}
function factory(_nada)
        return function() 
                local x = Session:tempo_map()
                local dialog_contents = {
                    { type = "heading", title = "Export Markers to MIDI Notes" },
                    { type = "file", key = "file", title = "Filename" },
                }
                local dialog_gui = LuaDialog.Dialog("Export Markers to MIDI Notes", dialog_contents)
                local results = dialog_gui:run()
                local z = io.open(results["file"], "w+")
                for location in Session:locations():list():iter() do
                        if location:is_mark() then
                                local temp = x:exact_beat_at_frame(location:start(), 0)
                                z:write(string.pack("H", math.floor(temp)))
                        end
                end
                z:close()
        end
end
