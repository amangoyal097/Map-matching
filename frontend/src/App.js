import { useState } from 'react'
import { MapContainer, TileLayer, useMap, useMapEvent } from 'react-leaflet'
import { GeoJSON } from 'react-leaflet'
import L from 'leaflet'
import sf from './map_data/boundary.json'
import './App.css'
import axios from 'axios'
import Loading from './components/Loading'
import Button from '@mui/material/Button'
import Alert from './components/Alert'
import Snackbar from '@mui/material/Snackbar'
import Grid from '@mui/material/Grid'

const mapBounds = [
  [37.6894651000000067, -122.513634099999976],
  [37.8323957999999863, -122.3277318999999892],
]

const App = () => {
  const [selecting, setSelecting] = useState(false)
  const [userMarker, setUserMarker] = useState([])
  const [data, setData] = useState({
    org: null,
    track: null,
    mapped: null,
  })
  const [loading, setLoading] = useState(false)

  const RenderBoundary = () => {
    const map = useMap()
    map.setMinZoom(13)
    return <GeoJSON key="boundary" data={sf} />
  }

  const Legend = () => {
    return (
      <Grid
        container
        p={2}
        justifyContent="space-between"
        alignItems="center"
        className="legend"
      >
        <Grid item xs={2}>
          <div
            style={{
              borderRadius: '10px',
              width: '10px',
              height: '10px',
              background: 'green',
            }}
          ></div>
        </Grid>
        <Grid item xs={9} className="time">
          Mapped Points
        </Grid>
        <Grid item xs={2}>
          <div
            style={{
              borderRadius: '10px',
              width: '10px',
              height: '10px',
              background: 'orange',
            }}
          ></div>
        </Grid>
        <Grid item xs={9} className="time">
          Original Points
        </Grid>
        <Grid item xs={2}>
          <div
            style={{
              width: '100%',
              height: '5px',
              background: '#3388ff',
            }}
          ></div>
        </Grid>
        <Grid item xs={9} className="time">
          Track
        </Grid>
      </Grid>
    )
  }

  const MapClick = () => {
    var circleStyle = {
      radius: 5,
      fillColor: '#ff7800',
      color: '#000',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8,
    }
    const map2 = useMapEvent('keydown', (e) => {
      if (selecting && e.originalEvent.key == 'q') {
        setSelecting(false)
        const coords = userMarker.map((marker) => [
          marker._latlng.lat,
          marker._latlng.lng,
        ])
        if (coords.length > 0) {
          const formData = new FormData()
          formData.append('coords', coords)
          setLoading(true)
          axios
            .post('http://localhost:5000/path', formData)
            .then((response) => {
              const track = L.geoJSON(JSON.parse(response.data.track), {
                pointToLayer: function (feature, latlng) {
                  return L.circleMarker(latlng, circleStyle)
                },
              })
              const org = L.geoJSON(JSON.parse(response.data.org), {
                pointToLayer: function (feature, latlng) {
                  return L.circleMarker(latlng, {
                    ...circleStyle,
                  })
                },
              })
              const mapped = L.geoJSON(JSON.parse(response.data.mapped), {
                pointToLayer: function (feature, latlng) {
                  return L.circleMarker(latlng, {
                    ...circleStyle,
                    fillColor: 'green',
                  })
                },
              })
              setData({
                track,
                org,
                mapped,
              })
              map.addLayer(track)
              map.addLayer(org)
              map.addLayer(mapped)
              setLoading(false)
            })
            .catch((err) => {
              console.log(err)
              setLoading(false)
            })
        }
      }
    })
    const map = useMapEvent('click', (e) => {
      if (selecting) {
        const tempMarker = L.marker(e.latlng)
        setUserMarker([...userMarker, tempMarker])
        map.addLayer(tempMarker)
      }
    })
    return null
  }

  const handleSnackClose = (_, reason) => {
    if (reason === 'clickaway') {
      return
    }
    setSelecting(false)
  }

  const submitFile = (file, map) => {
    var circleStyle = {
      radius: 5,
      fillColor: '#ff7800',
      color: '#000',
      weight: 1,
      opacity: 1,
      fillOpacity: 0.8,
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    axios
      .post('http://localhost:5000/gpx', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => {
        const track = L.geoJSON(JSON.parse(response.data.track), {
          pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, circleStyle)
          },
        })
        const org = L.geoJSON(JSON.parse(response.data.org), {
          pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
              ...circleStyle,
            })
          },
        })
        const mapped = L.geoJSON(JSON.parse(response.data.mapped), {
          pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
              ...circleStyle,
              fillColor: 'green',
            })
          },
        })
        setData({
          track,
          org,
          mapped,
        })
        map.addLayer(track)
        map.addLayer(org)
        map.addLayer(mapped)
        setLoading(false)
      })
      .catch((error) => {
        console.error(error)
        setLoading(false)
      })
  }

  const RenderUpload = () => {
    const map = useMap()
    return (
      <>
        <Button
          variant="contained"
          sx={{
            background: '#24a0ed',
            position: 'absolute',
            bottom: '3rem',
            left: '2rem',
            zIndex: 999,
          }}
          component="label"
        >
          UPLOAD GPX Trace
          <input
            type="file"
            onChange={(e) => {
              if (data.track) map.removeLayer(data.track)
              if (data.org) map.removeLayer(data.org)
              if (data.mapped) map.removeLayer(data.mapped)
              setData({ track: null, org: null, mapped: null })
              userMarker.forEach((marker) => map.removeLayer(marker))
              setUserMarker([])
              submitFile(e.target.files[0], map)
            }}
            hidden
            accept=".gpx"
          />
        </Button>
        {!selecting && (
          <Button
            variant="contained"
            sx={{
              background: '#24a0ed',
              position: 'absolute',
              bottom: '6rem',
              left: '2rem',
              zIndex: 999,
            }}
            component="label"
            onClick={() => {
              if (!selecting) {
                if (data.track) map.removeLayer(data.track)
                if (data.org) map.removeLayer(data.org)
                if (data.mapped) map.removeLayer(data.mapped)
                setData({ track: null, org: null, mapped: null })
                userMarker.forEach((marker) => map.removeLayer(marker))
                setUserMarker([])
                setSelecting(true)
              } else {
                setSelecting(false)
              }
            }}
          >
            Add Path
          </Button>
        )}
      </>
    )
  }

  return (
    <>
      {loading && <Loading />}
      {data.mapped !== null && <Legend />}
      <div>
        <MapContainer
          bounds={mapBounds}
          style={{
            height: '100vh',
            background: 'white',
          }}
          scrollWheelZoom={true}
          touchZoom={false}
          doubleClickZoom={false}
        >
          <RenderUpload />
          <Snackbar
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            open={selecting}
            onClose={handleSnackClose}
          >
            <Alert
              onClose={handleSnackClose}
              severity="info"
              sx={{ width: '100%', fontFamily: 'Montserrat' }}
            >
              Press q to complete path
            </Alert>
          </Snackbar>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            opacity={0.4}
          />
          <MapClick />
          <RenderBoundary />
        </MapContainer>
      </div>
    </>
  )
}

export default App
