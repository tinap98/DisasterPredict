import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const DonationForm = ({ userId }) => {
    const [amount, setAmount] = useState('');
    const [currency, setCurrency] = useState('USD');
    const [cardNumber, setCardNumber] = useState('•••• •••• •••• 1234');
    const [expiry, setExpiry] = useState('12/25');
    const [cvc, setCvc] = useState('•••');
    const [isProcessing, setIsProcessing] = useState(false);
    const [transaction, setTransaction] = useState(null);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

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
        <div className="donation-form">
            {!transaction ? (
                <form onSubmit={handleSubmit}>
                    <h2>Support Relief Efforts</h2>
                    {error && <div className="error-message">{error}</div>}
                    <div className="form-group">
                        <label>Amount:</label>
                        <input
                            type="number"
                            step="0.01"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            required
                            min="1"
                        />
                    </div>
                    
                    <div className="form-group">
                        <label>Currency:</label>
                        <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
                            <option value="USD">USD</option>
                            <option value="EUR">EUR</option>
                            <option value="GBP">GBP</option>
                        </select>
                    </div>

                    <div className="payment-details">
                        <h3>Payment Information</h3>
                        <div className="form-group">
                            <label>Card Number:</label>
                            <input
                                type="text"
                                value={cardNumber}
                                pattern="\d*"
                                disabled
                                placeholder="Mock payment disabled"
                            />
                        </div>
                        
                        <div className="form-group-row">
                            <div>
                                <label>Expiry:</label>
                                <input
                                    type="text"
                                    value={expiry}
                                    disabled
                                />
                            </div>
                            <div>
                                <label>CVC:</label>
                                <input
                                    type="text"
                                    value={cvc}
                                    disabled
                                />
                            </div>
                        </div>
                    </div>

                    <button type="submit" disabled={isProcessing}>
                        {isProcessing ? 'Processing...' : 'Donate Now'}
                    </button>
                    <p className="mock-notice">Note: This is a mock payment system. No real transactions will occur.</p>
                </form>
            ) : (
                <div className="donation-success">
                    <h2>Thank you for your generosity!💖</h2>
                    <p>We've successfully processed your donation of {transaction.amount} {transaction.currency}.</p>
                    <p>Transaction ID: {transaction.transaction_id}</p>
                    <button onClick={() => navigate('/')}>Return Home</button>
                </div>
            )}
        </div>
    );
};

export default DonationForm;