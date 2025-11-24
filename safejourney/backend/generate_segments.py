"""
Generate segments for India covering major cities and areas
This creates a grid of segments that cover the entire India region
"""

from sqlmodel import Session, select
from database import engine
from models import Segment
import json

def create_segments():
    """Create segments covering India"""
    
    session = Session(engine)
    
    # Check if segments already exist
    existing = session.exec(select(Segment)).first()
    if existing:
        print("✅ Segments already exist in database")
        session.close()
        return
    
    # Define segments for major Indian cities and regions
    # Format: (lat_min, lat_max, lon_min, lon_max, city_name)
    segments = [
        # Hyderabad region (Telangana)
        (17.3, 17.5, 78.3, 78.5, "Hyderabad Downtown"),
        (17.35, 17.65, 78.25, 78.55, "Hyderabad Metro"),
        (17.0, 17.8, 78.0, 79.0, "Greater Hyderabad"),
        
        # Bangalore region (Karnataka)
        (12.9, 13.1, 77.5, 77.7, "Bangalore Downtown"),
        (12.8, 13.2, 77.4, 77.8, "Bangalore Metro"),
        (12.5, 13.5, 77.0, 78.0, "Greater Bangalore"),
        
        # Delhi region
        (28.4, 28.6, 77.0, 77.2, "Delhi Downtown"),
        (28.3, 28.8, 76.8, 77.3, "Delhi Metro"),
        (28.0, 29.0, 76.5, 77.5, "Greater Delhi"),
        
        # Mumbai region (Maharashtra)
        (19.0, 19.2, 72.8, 73.0, "Mumbai Downtown"),
        (18.9, 19.3, 72.7, 73.1, "Mumbai Metro"),
        (18.5, 19.5, 72.3, 73.3, "Greater Mumbai"),
        
        # Pune region (Maharashtra)
        (18.5, 18.7, 73.8, 74.0, "Pune Downtown"),
        (18.3, 18.9, 73.6, 74.2, "Pune Metro"),
        (18.0, 19.0, 73.3, 74.3, "Greater Pune"),
        
        # Kolkata region (West Bengal)
        (22.5, 22.7, 88.3, 88.5, "Kolkata Downtown"),
        (22.3, 22.9, 88.1, 88.7, "Kolkata Metro"),
        (22.0, 23.0, 87.8, 88.8, "Greater Kolkata"),
        
        # Chennai region (Tamil Nadu)
        (13.0, 13.2, 80.2, 80.4, "Chennai Downtown"),
        (12.8, 13.4, 80.0, 80.6, "Chennai Metro"),
        (12.5, 13.5, 79.7, 80.7, "Greater Chennai"),
        
        # Jaipur region (Rajasthan)
        (26.9, 27.1, 75.7, 75.9, "Jaipur Downtown"),
        (26.7, 27.3, 75.5, 76.1, "Jaipur Metro"),
        (26.5, 27.5, 75.3, 76.3, "Greater Jaipur"),
        
        # Lucknow region (Uttar Pradesh)
        (26.8, 27.0, 80.9, 81.1, "Lucknow Downtown"),
        (26.6, 27.2, 80.7, 81.3, "Lucknow Metro"),
        (26.4, 27.4, 80.5, 81.5, "Greater Lucknow"),
        
        # Ahmedabad region (Gujarat)
        (23.1, 23.3, 72.5, 72.7, "Ahmedabad Downtown"),
        (22.9, 23.5, 72.3, 72.9, "Ahmedabad Metro"),
        (22.7, 23.7, 72.1, 73.1, "Greater Ahmedabad"),
        
        # Surat region (Gujarat)
        (21.1, 21.3, 72.8, 73.0, "Surat Downtown"),
        (20.9, 21.5, 72.6, 73.2, "Surat Metro"),
        (20.7, 21.7, 72.4, 73.4, "Greater Surat"),
        
        # Cochin region (Kerala)
        (9.9, 10.1, 76.2, 76.4, "Cochin Downtown"),
        (9.7, 10.3, 76.0, 76.6, "Cochin Metro"),
        (9.5, 10.5, 75.8, 76.8, "Greater Cochin"),
    ]
    
    created_count = 0
    for lat_min, lat_max, lon_min, lon_max, city_name in segments:
        segment = Segment(
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max,
            segment_name=city_name,
            active_user_count=0,
            safety_score=5.0,
            reports=json.dumps([]),
            report_count=0
        )
        session.add(segment)
        created_count += 1
    
    session.commit()
    session.close()
    
    print(f"✅ Created {created_count} segments for major Indian cities")
    print("\nSegments created:")
    for lat_min, lat_max, lon_min, lon_max, city_name in segments:
        print(f"  • {city_name}: ({lat_min}, {lon_min}) to ({lat_max}, {lon_max})")

if __name__ == "__main__":
    create_segments()
