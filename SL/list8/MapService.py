import folium
import tempfile


class MapService:
    def generate_map(self, lat: float, lon: float) -> str:
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon]).add_to(m)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as map_file:
            m.save(map_file)
            map_file.close()

            return 'file://' + map_file.name
