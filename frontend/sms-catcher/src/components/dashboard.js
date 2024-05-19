import React, { useState, useEffect } from 'react';
import fetchData from '../services/apiService';
import BarChart from './barChart';
import PieChart from './pieChart';
import LineGraph from './lineGraph';

const Dashboard = () => {
  const [dashboardInfo, setDashboardInfo] = useState({});
  const [error, setError] = useState(null);

  const fetchDashboardData = async () => {
    try {
      const data = await fetchData('http://127.0.0.1:8000/dashboard');
      setDashboardInfo(data);
      setError(null); // Clear any previous errors
    } catch (error) {
      console.error('Error fetching dashboard info:', error);
      setError(error.message || 'Failed to fetch dashboard info');
    }
  };

  useEffect(() => {
    fetchDashboardData(); // Initial fetch

    const interval = setInterval(fetchDashboardData, 60000); // Fetch data every minute

    return () => clearInterval(interval); // Clear interval on unmount
  }, []);

  // Extract data for the BarChart
  const barChartData = {
      labels: Object.keys(dashboardInfo.smishings_per_phone_number || {}),
      values: Object.values(dashboardInfo.smishings_per_phone_number || {}),
    };

  // Extract data for the LineGraphChart
  const lineGraphDataSmishDaily= {
    labels: Object.keys(dashboardInfo.daily_smishings || {}),
    values: Object.values(dashboardInfo.daily_smishings || {}),
  };

  // Extract data for the LineGraphChart
  const lineGraphDataSmishMonthly= {
    labels: Object.keys(dashboardInfo.monthly_smishings || {}),
    values: Object.values(dashboardInfo.monthly_smishings || {}),
  };

  // Extract data for the LineGraphChart
  const lineGraphDataSmishYearly = {
    labels: Object.keys(dashboardInfo.yearly_smishings || {}),
    values: Object.values(dashboardInfo.yearly_smishings || {}),
  };

  // Extract data for the LineGraphChart
  const lineGraphDataAllTextsMonthly = {
    labels: Object.keys(dashboardInfo.monthly_messages || {}),
    values: Object.values(dashboardInfo.monthly_messages || {}),
  };

  // Extract data for the LineGraphChart
  const lineGraphDataAllTextsYearly = {
    labels: Object.keys(dashboardInfo.yearly_messages || {}),
    values: Object.values(dashboardInfo.yearly_messages || {}),
  };

  return (
    <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
      <div className="bg-gray-200 p-4 rounded-md">
        <h3 className="text-lg font-semibold mb-2">Smishing Messages Captured Last Week</h3>
        {/* Updated BarChart component with data prop */}
        <BarChart data={barChartData} />
      </div>
      <div className="bg-gray-200 p-4 rounded-md" style={{ maxWidth: '70%', maxHeight: '60%' }}>
        <h3 className="text-lg font-semibold mb-2">Smishing vs Legitimate messages captured</h3>
        <PieChart
          data={{
            labels: ['Smishing', 'Legitimate'],
            values: [dashboardInfo.smishing_count || 0, dashboardInfo.legitimate_count || 0],
          }}
        />
      </div>
      <div className="bg-gray-200 p-4 rounded-md">
        <h3 className="text-lg font-semibold mb-2">Smishings Captured last Week</h3>
        <LineGraph
          data={lineGraphDataSmishDaily}
        />
      </div>
      <div className="bg-gray-200 p-4 rounded-md">
        <h3 className="text-lg font-semibold mb-2">Smishings Captured per month</h3>
        <LineGraph
          data={lineGraphDataSmishMonthly}
        />
      </div>
      <div className="bg-gray-200 p-4 rounded-md">
        <h3 className="text-lg font-semibold mb-2">Smishings Captured per year</h3>
        <LineGraph
          data={lineGraphDataSmishYearly}
        />
      </div>
      <div className="bg-gray-200 p-4 rounded-md">
        <h3 className="text-lg font-semibold mb-2">Messages Captured per month</h3>
        <LineGraph
          data={lineGraphDataAllTextsMonthly}
        />
      </div>
      <div className="bg-gray-200 p-4 rounded-md">
        <h3 className="text-lg font-semibold mb-2">Messages Captured per year</h3>
        <LineGraph
          data={lineGraphDataAllTextsYearly}
        />
      </div>
      <div className="bg-gray-200 p-4 rounded-md">
        <h2>Dashboard Information:</h2>
        {error && <p>Error: {error}</p>}
        {dashboardInfo ? (
          <pre>{JSON.stringify(dashboardInfo, null, 2)}</pre>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
