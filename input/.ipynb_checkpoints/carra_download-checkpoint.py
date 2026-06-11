import cdsapi

dataset = "reanalysis-pan-carra"
request = {
    "level_type": "single_levels",
    "variable": [
        "10m_u_component_of_wind",
        "10m_v_component_of_wind",
        "10m_wind_direction",
        "10m_wind_speed"
    ],
    "product_type": "analysis",
    "time": [
        "00:00", "03:00", "06:00",
        "09:00", "12:00", "15:00",
        "18:00", "21:00"
    ],
    "year": ["2025"],
    "month": [
        "09", "10", "11",
        "12"
    ],
    "day": [
        "01", "02", "03",
        "04", "05", "06",
        "07", "08", "09",
        "10", "11", "12",
        "13", "14", "15",
        "16", "17", "18",
        "19", "20", "21",
        "22", "23", "24",
        "25", "26", "27",
        "28", "29", "30",
        "31"
    ],
    "data_format": "grib",
    "area": [75, -80, 69, -40]
}

client = cdsapi.Client()
client.retrieve(dataset, request).download()
