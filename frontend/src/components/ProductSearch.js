
import React, { useState } from 'react';
import Plot from 'react-plotly.js';

const API_BASE_URL = 'http://localhost:8000'; // Adjust if your backend is elsewhere

function ProductSearch() {
    const [query, setQuery] = useState('');
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showAI, setShowAI] = useState(false);

    const handleSearch = async () => {
        if (!query) return;
        setLoading(true);
        setError(null);
        setProducts([]);

        const endpoint = showAI ? `/api/products/${query}/ai` : `/api/products/${query}`;

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            setProducts(data);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    // --- Chart Data Preparation ---
    const priceData = products.map(p => {
        try {
            return parseFloat(p.price?.replace('$', ''));
        } catch {
            return null;
        }
    }).filter(p => p !== null);

    const aiScatterData = showAI ? products.map(p => ({
        x: p.ai_analysis?.potential_margin,
        y: p.ai_analysis?.market_demand,
        text: p.title,
        type: 'scatter',
        mode: 'markers',
        marker: { size: 12, color: 'rgba(255, 99, 132, 0.6)' },
    })) : [];

    return (
        <div className="container mx-auto p-4 font-sans">
            <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">Dropshipping Product Scanner</h1>
            
            {/* Search Bar */}
            <div className="flex flex-col md:flex-row gap-4 mb-6 justify-center items-center">
                <input 
                    type="text" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter a product to search..."
                    className="w-full md:w-1/2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button 
                    onClick={handleSearch}
                    disabled={loading}
                    className="w-full md:w-auto px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
                >
                    {loading ? 'Searching...' : 'Search'}
                </button>
            </div>

            {/* AI Toggle */}
            <div className="flex items-center justify-center mb-8">
                <label className="flex items-center cursor-pointer">
                    <div className="relative">
                        <input type="checkbox" checked={showAI} onChange={() => setShowAI(!showAI)} className="sr-only" />
                        <div className="block bg-gray-600 w-14 h-8 rounded-full"></div>
                        <div className={`dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition-transform ${showAI ? 'transform translate-x-full bg-green-400' : ''}`}></div>
                    </div>
                    <div className="ml-3 text-gray-700 font-medium">
                        Enable AI Analysis
                    </div>
                </label>
            </div>

            {/* Error and Loading Messages */}
            {error && <p className="text-center text-red-500">Error: {error}</p>}
            {loading && <p className="text-center text-blue-500">Loading data...</p>}

            {/* Results Table */}
            {products.length > 0 && (
                <div className="overflow-x-auto shadow-lg rounded-lg mb-8">
                    <table className="min-w-full bg-white">
                        <thead className="bg-gray-800 text-white">
                            <tr>
                                <th className="text-left py-3 px-4 uppercase font-semibold text-sm">Product Title</th>
                                <th className="text-left py-3 px-4 uppercase font-semibold text-sm">Price</th>
                                <th className="text-left py-3 px-4 uppercase font-semibold text-sm">Source</th>
                                {showAI && <th className="text-left py-3 px-4 uppercase font-semibold text-sm">Margin</th>}
                                {showAI && <th className="text-left py-3 px-4 uppercase font-semibold text-sm">Demand</th>}
                                {showAI && <th className="text-left py-3 px-4 uppercase font-semibold text-sm">Reliability</th>}
                            </tr>
                        </thead>
                        <tbody className="text-gray-700">
                            {products.map((product, index) => (
                                <tr key={index} className="border-b border-gray-200 hover:bg-gray-100">
                                    <td className="py-3 px-4"><a href={product.link} target="_blank" rel="noopener noreferrer" className="hover:text-blue-600">{product.title}</a></td>
                                    <td className="py-3 px-4">{product.price || 'N/A'}</td>
                                    <td className="py-3 px-4">{product.source}</td>
                                    {showAI && <td className="py-3 px-4">{product.ai_analysis?.potential_margin || 'N/A'}</td>}
                                    {showAI && <td className="py-3 px-4">{product.ai_analysis?.market_demand || 'N/A'}</td>}
                                    {showAI && <td className="py-3 px-4">{product.ai_analysis?.seller_reliability || 'N/A'}</td>}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Charts */}
            {products.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="bg-white p-4 rounded-lg shadow-lg">
                        <h2 className="text-xl font-bold mb-4 text-center">Price Distribution</h2>
                        <Plot
                            data={[{
                                x: priceData,
                                type: 'box',
                                name: 'Price'
                            }]}
                            layout={{ title: 'Product Price Box Plot' }}
                            className="w-full h-full"
                        />
                    </div>
                    {showAI && (
                        <div className="bg-white p-4 rounded-lg shadow-lg">
                            <h2 className="text-xl font-bold mb-4 text-center">AI Analysis</h2>
                            <Plot
                                data={aiScatterData}
                                layout={{ 
                                    title: 'AI Metrics (Margin vs. Demand)',
                                    xaxis: { title: 'Potential Margin' },
                                    yaxis: { title: 'Market Demand' }
                                }}
                                className="w-full h-full"
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default ProductSearch;
