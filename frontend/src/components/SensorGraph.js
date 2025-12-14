import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import axios from "axios";

const SensorGraph = ({ liveData }) => {
  const [data, setData] = useState([]);

  // Helper function to format the timestamp
  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return new Intl.DateTimeFormat("en-GB", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    }).format(date);
  };

  useEffect(() => {
    const fetchGraphData = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/v1/sensors/latest");

        const arr = res.data.data || [];

        if (Array.isArray(arr)) {
          // Format the timestamps of the fetched data
          const formattedData = arr.map(item => ({
            ...item,
            timestamp: formatTimestamp(item.timestamp),
          }));
          setData(formattedData.slice(-20));
        }
      } catch (err) {
        console.error("Failed to load graph data:", err);
      }
    };

    fetchGraphData();
    const interval = setInterval(fetchGraphData, 5000);

    return () => clearInterval(interval);
  }, []);

  // Handle MQTT live updates
  useEffect(() => {
    if (!liveData) return;

    const withFormattedTimestamp = {
      ...liveData,
      timestamp: formatTimestamp(liveData.timestamp || new Date().toISOString()),
    };

    setData(prev => {
      const updated = [...prev, withFormattedTimestamp];
      return updated.slice(-20);
    });
  }, [liveData]);

  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="card">
        <h2>Live Sensor Graph</h2>
        <p className="label">No data yet...</p>
      </div>
    );
  }

  // Calculate Y axis space
  const yValues = data.flatMap(d => [d.temperature, d.humidity]);
  const yMin = Math.min(...yValues);
  const yMax = Math.max(...yValues);
  const yPadding = (yMax - yMin) * 0.1 || 1; // 10% margin, minimum 1

  return (
    <div className="card" style={{ height: "400px" }}>
      <h2>Live Sensor Graph</h2>
      <ResponsiveContainer width="95%" height="80%">
        <LineChart data={data.slice().reverse()}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" reversed={true} />
          <YAxis domain={[yMin - yPadding, yMax + yPadding]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="temperature" stroke="#e00000ff" />
          <Line type="monotone" dataKey="humidity" stroke="#1f7bf3ff" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SensorGraph;
