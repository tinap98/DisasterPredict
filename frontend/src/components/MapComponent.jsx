import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import MarkerClusterGroup from 'react-leaflet-markercluster';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const MapBounds = ({ disasters }) => {
  const map = useMap();

  const bounds = disasters
    .flatMap((event) => event.geometry)
    .map((geo) => [geo.coordinates[1], geo.coordinates[0]]); 
  if (bounds.length > 0) {
    map.fitBounds(bounds, { padding: [50, 50] }); 
  }

  return null;
};

const MapComponent = ({ disasters }) => {
  return (
    <div style={{ height: '70vh', width: '100%' }}>
      <MapContainer
        center={[20, 0]}
        zoom={2}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='© OpenStreetMap'
        />

        <MapBounds disasters={disasters} />

        <MarkerClusterGroup>
          {disasters?.map((event) =>
            event.geometry?.map((geo, geoIndex) => {
              if (!geo.coordinates || geo.coordinates.length !== 2) {
                console.warn('Invalid coordinates:', geo.coordinates);
                return null;
              }

              const [lon, lat] = geo.coordinates;

              return (
                <Marker
                  key={`${event.id}-${geoIndex}`}
                  position={[lat, lon]}
                >
                  <Popup>
                    <h3>{event.title}</h3>
                    <p>Category: {event.categories[0]?.title}</p>
                    <p>Date: {new Date(geo.date).toLocaleDateString()}</p>
                    {event.sources?.[0]?.url && (
                      <a
                        href={event.sources[0].url}
                        target="_blank"
                        rel="noreferrer"
                      >
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
  );
};

export default MapComponent;