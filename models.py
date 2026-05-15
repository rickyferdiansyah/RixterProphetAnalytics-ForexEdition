# models.py - RixterProphet Analytics: Forex Edition
# LSTM Model Architectures for Forex Prediction

import torch
import torch.nn as nn

class VanillaLSTM(nn.Module):
    """
    Vanilla LSTM - Simple and effective for forex time series
    Single layer LSTM with dropout for regularization
    """
    def __init__(self, input_size, hidden_size, output_size, dropout=0.1):
        super(VanillaLSTM, self).__init__()
        self.hidden_size = hidden_size
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=1,
            batch_first=True,
            dropout=0  # Dropout only works with multiple layers
        )
        
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights with Xavier/Glorot initialization"""
        for name, param in self.lstm.named_parameters():
            if 'weight' in name:
                nn.init.xavier_uniform_(param)
            elif 'bias' in name:
                nn.init.constant_(param, 0.0)
        
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.constant_(self.fc.bias, 0.0)
    
    def forward(self, x):
        # x shape: (batch_size, seq_len, input_size)
        lstm_out, _ = self.lstm(x)
        
        # Take only the last output
        last_output = lstm_out[:, -1, :]
        
        # Apply dropout
        out = self.dropout(last_output)
        
        # Fully connected layer
        out = self.fc(out)
        
        return out


class BidirectionalLSTM(nn.Module):
    """
    Bidirectional LSTM - Better pattern recognition for forex
    Processes sequence in both directions for enhanced context
    """
    def __init__(self, input_size, hidden_size, output_size, dropout=0.1):
        super(BidirectionalLSTM, self).__init__()
        self.hidden_size = hidden_size
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=1,
            batch_first=True,
            bidirectional=True,
            dropout=0
        )
        
        self.dropout = nn.Dropout(dropout)
        # Note: bidirectional doubles the hidden size
        self.fc = nn.Linear(hidden_size * 2, output_size)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights with Xavier/Glorot initialization"""
        for name, param in self.lstm.named_parameters():
            if 'weight' in name:
                nn.init.xavier_uniform_(param)
            elif 'bias' in name:
                nn.init.constant_(param, 0.0)
        
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.constant_(self.fc.bias, 0.0)
    
    def forward(self, x):
        # x shape: (batch_size, seq_len, input_size)
        lstm_out, _ = self.lstm(x)
        
        # Take only the last output (which has both forward and backward context)
        last_output = lstm_out[:, -1, :]
        
        # Apply dropout
        out = self.dropout(last_output)
        
        # Fully connected layer
        out = self.fc(out)
        
        return out


class LSTMAttention(nn.Module):
    """
    LSTM with Attention Mechanism (Bonus Model)
    Can be added later for enhanced prediction
    """
    def __init__(self, input_size, hidden_size, output_size, dropout=0.1):
        super(LSTMAttention, self).__init__()
        self.hidden_size = hidden_size
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=1,
            batch_first=True,
            bidirectional=False
        )
        
        # Attention layer
        self.attention = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        )
        
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        
        self._init_weights()
    
    def _init_weights(self):
        """Initialize weights"""
        for name, param in self.lstm.named_parameters():
            if 'weight' in name:
                nn.init.xavier_uniform_(param)
            elif 'bias' in name:
                nn.init.constant_(param, 0.0)
        
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.constant_(self.fc.bias, 0.0)
    
    def forward(self, x):
        # x shape: (batch_size, seq_len, input_size)
        lstm_out, _ = self.lstm(x)
        
        # Calculate attention weights
        attention_weights = self.attention(lstm_out)
        attention_weights = torch.softmax(attention_weights, dim=1)
        
        # Apply attention
        context_vector = torch.sum(attention_weights * lstm_out, dim=1)
        
        # Dropout and FC
        out = self.dropout(context_vector)
        out = self.fc(out)
        
        return out
