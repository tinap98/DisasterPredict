const API_URL = 'https://eonet.gsfc.nasa.gov/api/v3/events';

const CATEGORY_IDS = {
  wildfires: 8,
  severeStorms: 10,
  volcanoes: 12,
  earthquakes: 16,
  landslides: 14,
  floods: 9
};

export const fetchDisasters = async (category) => {
  try {
    const params = new URLSearchParams();
    
    if (category && CATEGORY_IDS[category]) {
      params.append('categories', CATEGORY_IDS[category]);
    }

    const response = await fetch(`${API_URL}?${params}`);
    const data = await response.json();
    
    const events = data.events || data;
    console.log('Processed events:', events);
    return Array.isArray(events) ? events : [];
  } catch (error) {
    console.error('Failed to fetch data:', error);
    return [];
  }
};