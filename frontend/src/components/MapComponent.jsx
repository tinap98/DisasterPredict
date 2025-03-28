import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import MarkerClusterGroup from "react-leaflet-markercluster";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import { fetchDisasters } from "./nasa";
import "../index.css";

// Fix Leaflet marker issue with missing icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

// Component to adjust map bounds based on disaster markers
const MapBounds = ({ disasters }) => {
  const map = useMap();

  useEffect(() => {
    if (disasters.length > 0) {
      const bounds = disasters.flatMap((event) => event.geometry).map((geo) => [geo.coordinates[1], geo.coordinates[0]]);
      if (bounds.length > 0) {
        map.fitBounds(bounds, { padding: [50, 50] });
      }
    }
  }, [disasters, map]);

  return null;
};

const MapComponent = () => {
  const [disasters, setDisasters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState("");

  useEffect(() => {
    loadData(selectedCategory);
  }, [selectedCategory]);

  const loadData = async (category) => {
    try {
      setLoading(true);
      const data = await fetchDisasters(category);

      if (data.length === 0) {
        setError("No current disasters found");
      } else {
        setError(null);
      }

      setDisasters(data);
    } catch (err) {
      setError("Failed to load disaster data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center w-full min-h-screen p-6 bg-gray-100">
      {/* Header */}
      <h1 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        NASA Real-Time Disaster Tracker
      </h1>

      {/* Disaster Category Filter */}
      <div className="w-full max-w-2xl flex flex-col sm:flex-row items-center justify-center gap-4 mb-6">
        <label className="font-semibold text-gray-700 text-center sm:text-left">
          Disaster Category:
        </label>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="border p-2 rounded-md w-40 bg-white shadow-md text-center"
        >
          <option value="">All Disasters</option>
          <option value="wildfires">Wildfires</option>
          <option value="severeStorms">Severe Storms</option>
          <option value="volcanoes">Volcanoes</option>
          <option value="earthquakes">Earthquakes</option>
          <option value="landslides">Landslides</option>
          <option value="floods">Floods</option>
        </select>
      </div>

      {/* Loading and Error Messages */}
      {loading && (
        <div className="text-lg font-semibold text-blue-600 text-center">
          Loading live data from NASA...
        </div>
      )}
      {error && (
        <div className="text-lg text-red-600 font-semibold text-center mt-2">
          {error} - Try refreshing or check{" "}
          <a
            href="https://eonet.gsfc.nasa.gov/"
            target="_blank"
            rel="noreferrer"
            className="text-blue-500 underline"
          >
            NASA EONET
          </a>
        </div>
      )}

      {/* Map Display */}
      {!loading && !error && (
        <div className="w-full max-w-5xl h-[70vh] shadow-lg rounded-lg overflow-hidden mt-6">
          <MapContainer center={[20, 0]} zoom={2} className="h-full w-full">
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="© OpenStreetMap" />
            <MapBounds disasters={disasters} />

            <MarkerClusterGroup>
              {disasters.map((event) =>
                event.geometry.map((geo, geoIndex) => {
                  if (!geo.coordinates || geo.coordinates.length !== 2) {
                    console.warn("Invalid coordinates:", geo.coordinates);
                    return null;
                  }

                  const [lon, lat] = geo.coordinates;

                  return (
                    <Marker key={`${event.id}-${geoIndex}`} position={[lat, lon]}>
                      <Popup>
                        <h3 className="font-bold">{event.title}</h3>
                        <p><strong>Category:</strong> {event.categories[0]?.title}</p>
                        <p><strong>Date:</strong> {new Date(geo.date).toLocaleDateString()}</p>
                        {event.sources?.[0]?.url && (
                          <a href={event.sources[0].url} target="_blank" rel="noreferrer" className="text-blue-500 underline">
                            More info
                          </a>
                        )}
                      </Popup>
                    </Marker>
                  );
                })
              )}
            </MarkerClusterGroup>
          </MapContainer>
        </div>
      )}
    </div>
  );
};

export default MapComponent;
