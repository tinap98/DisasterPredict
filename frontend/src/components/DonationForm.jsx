import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const DonationForm = ({ userId }) => {
    const [amount, setAmount] = useState('');
    const [currency, setCurrency] = useState('USD');
    const [isProcessing, setIsProcessing] = useState(false);
    const [transaction, setTransaction] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!userId) {
            navigate('/login');
        }
    }, [userId, navigate]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsProcessing(true);
        setError(null);

        try {
            const response = await fetch('http://localhost:5000/api/donate', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({
                    user_id: userId,
                    amount: parseFloat(amount),
                    currency,
                    payment_method: 'credit_card'
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Donation failed');
            }

            const result = await response.json();
            setTransaction(result);
        } catch (error) {
            console.error('Donation error:', error);
            setError(error.message || 'Failed to process donation. Please try again.');
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="flex justify-center items-center py-10 bg-black">
            <div className="bg-black bg-opacity-90 shadow-lg rounded-2xl p-6 w-full max-w-md border-2 border-[#FFC115] my-10">
                {!transaction ? (
                    <form onSubmit={handleSubmit} className="space-y-4 text-white">
                        <h2 className="text-2xl font-bold text-[#FFC115] text-center">Support Relief Efforts</h2>
                        {error && <div className="text-red-500 text-sm text-center">{error}</div>}
                        
                        <div className="space-y-2">
                            <label className="block text-gray-300">Amount:</label>
                            <input
                                type="number"
                                step="0.01"
                                value={amount}
                                onChange={(e) => setAmount(e.target.value)}
                                required
                                min="1"
                                className="w-full px-3 py-2 border border-gray-600 rounded-md focus:ring-2 focus:ring-[#FFC115] outline-none bg-gray-800 text-white"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="block text-gray-300">Currency:</label>
                            <select 
                                value={currency} 
                                onChange={(e) => setCurrency(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-600 rounded-md focus:ring-2 focus:ring-[#FFC115] outline-none bg-gray-800 text-white"
                            >
                                <option value="USD">USD</option>
                                <option value="EUR">EUR</option>
                                <option value="GBP">GBP</option>
                            </select>
                        </div>

                        <div className="bg-gray-900 p-4 rounded-md shadow-sm border border-gray-700">
                            <h3 className="text-lg font-semibold text-[#FFC115]">Payment Information</h3>
                            <div className="mt-2">
                                <label className="block text-gray-300">Card Number:</label>
                                <input
                                    type="text"
                                    value="•••• •••• •••• 1234"
                                    disabled
                                    className="w-full px-3 py-2 bg-gray-700 text-gray-400 rounded-md cursor-not-allowed"
                                />
                            </div>

                            <div className="flex justify-between mt-2 space-x-2">
                                <div className="flex-1">
                                    <label className="block text-gray-300">Expiry:</label>
                                    <input
                                        type="text"
                                        value="12/25"
                                        disabled
                                        className="w-full px-3 py-2 bg-gray-700 text-gray-400 rounded-md cursor-not-allowed"
                                    />
                                </div>
                                <div className="flex-1">
                                    <label className="block text-gray-300">CVC:</label>
                                    <input
                                        type="text"
                                        value="•••"
                                        disabled
                                        className="w-full px-3 py-2 bg-gray-700 text-gray-400 rounded-md cursor-not-allowed"
                                    />
                                </div>
                            </div>
                        </div>

                        <button 
                            type="submit" 
                            disabled={isProcessing || !amount}
                            className="w-full py-3 bg-[#FFC115] text-black font-semibold rounded-lg shadow-md hover:bg-amber-500 transition-all duration-200 disabled:bg-gray-400"
                        >
                            {isProcessing ? 'Processing...' : 'Donate Now'}
                        </button>
                        <p className="text-xs text-gray-400 text-center mt-2">Note: This is a mock payment system. No real transactions will occur.</p>
                    </form>
                ) : (
                    <div className="text-center">
                        <h2 className="text-2xl font-bold text-[#FFC115]">Thank you for your generosity! 💖</h2>
                        <p className="text-gray-300 mt-2">We've successfully processed your donation of <span className="font-semibold text-white">{transaction.amount} {transaction.currency}</span>.</p>
                        <p className="text-gray-400 text-sm">Transaction ID: {transaction.transaction_id}</p>
                        <button 
                            onClick={() => navigate('/home')}
                            className="mt-4 px-6 py-2 bg-[#FFC115] text-black font-semibold rounded-lg shadow-md hover:bg-amber-500 transition-all duration-200"
                        >
                            Return Home
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DonationForm;
