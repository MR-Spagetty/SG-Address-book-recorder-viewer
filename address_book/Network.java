package address_book;

import java.io.File;
import java.nio.file.InvalidPathException;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Set;

public class Network {
    private Set<Glyph> glyphs = new HashSet<>();
    public final DeviceTypes networkType;
    public final String networkName;

    public Network(DeviceTypes type, String name) {
        this.networkType = type;
        this.networkName = name;
        Path typePath = switch (type) {
        case STARGATE -> Glyph.GLYPHS_DIR.resolve("SG");
        case TRANSPORT_RINGS -> Glyph.GLYPHS_DIR.resolve("TR");
        default -> throw new IllegalArgumentException("Unexpected value: " + type);
        };
        try {
            File[] glyphFiles = new File(typePath.resolve(name).toUri()).listFiles();
            for (File glyphFile : glyphFiles) {
                String fname = glyphFile.getName();
                int separatorIndex = fname.indexOf(".");
                // get the id of the glyph
                int id = Integer.parseInt(fname.substring(0, separatorIndex));
                // get the name of the glyph
                String glyphName = fname.substring(separatorIndex + 1,
                        fname.indexOf(".", separatorIndex + 1));
                this.glyphs.add(new Glyph(glyphName, id, glyphFile.toPath()));
            }
        } catch (InvalidPathException e) {
            // TODO impliment error message here for unknown glyph types
        }
    }
}
