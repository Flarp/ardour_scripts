---- this header is (only) required to save the script
-- ardour { ["type"] = "Snippet", name = "" }
-- function factory () return function () -- -- end end
ardour {
    ["type"] = "EditorAction",
    name = "Export Ranges to MIDI Notes",
    author = "Flarp",
    license = "BSD",
    description = "Export every range to a single note in a MIDI file",
}
function factory(_nada)
        return function() 
                local x = Session:tempo_map()
                local dialog_contents = {
                    { type = "heading", title = "Export Ranges to MIDI Notes" },
                    { type = "file", key = "file", title = "Filename" },
                }
                local dialog_gui = LuaDialog.Dialog("Export Ranges to MIDI Notes", dialog_contents)
                local results = dialog_gui:run()
                local z = io.open(results["file"], "w+")
                for location in Session:locations():list():iter() do
                        if location:is_range_marker() then
                                local start = location:start()
                                local beat_start = x:exact_beat_at_frame(start, 0)
                                local beat_end = x:exact_beat_at_frame(start + location:length(), 0)
                                z:write(string.pack("d", beat_start))
                                z:write(string.pack("d", beat_end))
                        end
                end
                z:close()
        end
end
