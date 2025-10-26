import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useSocket } from '../contexts/SocketContext';
import axios from 'axios';
import toast from 'react-hot-toast';
import {
  Send,
  Shield,
  Eye,
  Timer,
  Trash2,
  Users,
  Search,
  RefreshCw,
  AlertTriangle,
  Lock
} from 'lucide-react';

const Chat = () => {
  const { user, logout } = useAuth();
  const { connected, threatLevel } = useSocket();
  const [messages, setMessages] = useState([]);
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [newMessage, setNewMessage] = useState('');
  const [selfDestructTime, setSelfDestructTime] = useState(60); // ✅ Default 1 minute
  const [readOnce, setReadOnce] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  const [unreadCounts, setUnreadCounts] = useState({});
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadUsers();
    loadMessages();
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages]);

  useEffect(() => {
    const interval = setInterval(() => selectedUser && loadMessages(), 2000);
    return () => clearInterval(interval);
  }, [selectedUser]);

  useEffect(() => {
    const interval = setInterval(loadUsers, 10000);
    return () => clearInterval(interval);
  }, []);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

  const loadUsers = async () => {
    try {
      const res = await axios.get('/chat/users');
      setUsers(res.data.users);
    } catch {
      toast.error('Failed to load users');
    }
  };

  const loadMessages = async () => {
    try {
      let res;
      if (selectedUser) {
        res = await axios.get(`/chat/conversation/${selectedUser._id}`);
        setMessages(res.data.messages);
        setUnreadCounts(prev => ({ ...prev, [selectedUser._id]: 0 }));
      } else {
        res = await axios.get('/chat/receive');
        setMessages(res.data.messages);
        const counts = {};
        res.data.messages.forEach(msg => {
          if (msg.sender_id !== user.id && !msg.read) {
            counts[msg.sender_id] = (counts[msg.sender_id] || 0) + 1;
          }
        });
        setUnreadCounts(counts);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!newMessage.trim() || !selectedUser) return;
    setLoading(true);
    try {
      const res = await axios.post('/chat/send', {
        recipient_id: selectedUser._id,
        message: newMessage,
        self_destruct_time: selfDestructTime,
        read_once: readOnce
      });
      if (res.data.threat_score > 70) toast.error(`High threat detected: ${res.data.threat_score}`);
      setNewMessage('');
      setReadOnce(false);
      loadMessages();
      toast.success(`Message sent securely (self-destruct in ${selfDestructTime / 60} min)`);
    } catch {
      toast.error('Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const deleteMessage = async (messageId) => {
    try {
      await axios.delete(`/delete/message/${messageId}`);
      setMessages(messages.filter(m => m.id !== messageId));
      toast.success('Message deleted');
    } catch {
      toast.error('Failed to delete message');
    }
  };

  const getThreatLevelColor = (level) =>
    level > 70 ? 'text-red-400' : level > 40 ? 'text-yellow-400' : 'text-green-400';

  const getThreatLevelText = (level) =>
    level > 70 ? 'HIGH' : level > 40 ? 'MEDIUM' : 'LOW';

  const formatTime = (timestamp) => new Date(timestamp).toLocaleTimeString();

  const filteredUsers = users.filter(u => u.username.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <div className="h-screen flex bg-gradient-to-b from-blue-50 via-white to-pink-50">
      {/* Sidebar */}
      <div className="w-80 bg-white rounded-r-2xl shadow-lg flex flex-col border border-gray-200 overflow-hidden">
        {/* Encryption Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-pink-400 mr-2" />
              <h1 className="text-xl font-bold text-gray-800">Encryption</h1>
            </div>
            <button onClick={() => {}} className="p-2 hover:bg-gray-100 rounded-lg transition">
              <Lock className="h-5 w-5 text-gray-400" />
            </button>
          </div>
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center">
              <div className={`w-2 h-2 rounded-full mr-2 ${connected ? 'bg-green-400' : 'bg-red-400'}`}></div>
              <span className="text-gray-500">{connected ? 'Connected' : 'Disconnected'}</span>
            </div>
            <div className="flex items-center">
              <AlertTriangle className="h-4 w-4 mr-1 text-gray-400" />
              <span className={`${getThreatLevelColor(threatLevel)} text-xs font-medium`}>{getThreatLevelText(threatLevel)}</span>
            </div>
          </div>
        </div>

        {/* User Info */}
        <div className="p-4 border-b border-gray-200 flex items-center">
          <div className="w-10 h-10 bg-pink-400 rounded-full flex items-center justify-center mr-3 text-white font-medium">{user.username.charAt(0).toUpperCase()}</div>
          <div>
            <p className="font-medium text-gray-800">{user.username}</p>
            <p className="text-xs text-gray-400">Online</p>
          </div>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-gray-200 flex space-x-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search users..."
              className="w-full pl-10 pr-3 py-2 rounded-lg border border-gray-300 text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent transition duration-200 text-sm"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button onClick={loadUsers} className="px-3 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition" title="Refresh">
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>

        {/* Users List */}
        <div className="flex-1 overflow-y-auto p-2">
          <h3 className="text-sm font-medium text-gray-500 mb-2 px-2">Active Users ({filteredUsers.length})</h3>
          {filteredUsers.length > 0 ? (
            filteredUsers.map(u => (
              <button
                key={u._id}
                onClick={() => setSelectedUser(u)}
                className={`w-full flex items-center p-3 rounded-lg mb-1 transition-colors ${selectedUser?._id === u._id ? 'bg-pink-400 text-white' : 'hover:bg-gray-100 text-gray-800'}`}
              >
                <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center mr-3 text-sm font-medium">{u.username.charAt(0).toUpperCase()}</div>
                <div className="flex-1 text-left">
                  <p className="font-medium">{u.username}</p>
                  <p className="text-xs opacity-70">{u.is_admin ? 'Admin' : 'User'}</p>
                </div>
                <div className="flex items-center space-x-1">
                  {unreadCounts[u._id] > 0 && (
                    <span className="text-xs bg-red-400 text-white rounded-full px-2 py-0.5">{unreadCounts[u._id]}</span>
                  )}
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                </div>
              </button>
            ))
          ) : (
            <div className="text-center py-8 text-gray-400">
              <Users className="h-12 w-12 mx-auto mb-4" />
              <p className="text-sm">{searchTerm ? 'No users found' : 'No other users available'}</p>
            </div>
          )}
        </div>

        {/* Logout */}
        <div className="p-4 border-t border-gray-200">
          <button onClick={logout} className="w-full py-2 rounded-lg bg-gradient-to-r from-pink-400 to-blue-400 text-white font-semibold shadow hover:shadow-lg transition">Logout</button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {selectedUser ? (
          <>
            {/* Header */}
            <div className="p-4 border-b border-gray-200 bg-white flex items-center justify-between rounded-t-lg shadow-sm">
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center mr-3 text-gray-800 font-medium">{selectedUser.username.charAt(0).toUpperCase()}</div>
                <div>
                  <h2 className="font-medium text-gray-800">{selectedUser.username}</h2>
                  <p className="text-xs text-gray-500">End-to-end encrypted</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <Lock className="h-4 w-4 text-green-400" />
                <span className="text-xs text-green-400">Encrypted</span>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-white to-blue-50">
              {messages.map(message => (
                <div key={message.id} className={`flex ${message.sender_id === user.id ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-3 rounded-lg max-w-xs ${message.sender_id === user.id ? 'bg-pink-400 text-white' : 'bg-gray-100 text-gray-800'}`}>
                    <p className="text-sm">{message.content}</p>
                    <div className="flex items-center justify-between mt-1 text-xs opacity-70">
                      <span>{formatTime(message.timestamp)}</span>
                      <div className="flex items-center space-x-1">
                        {message.read_once && <Eye className="h-3 w-3" />}
                        {message.sender_id === user.id && (
                          <button onClick={() => deleteMessage(message.id)} className="hover:text-red-400 transition">
                            <Trash2 className="h-3 w-3" />
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-gray-200 bg-white flex flex-col space-y-2 rounded-b-lg shadow-sm">
              <form onSubmit={sendMessage} className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Type your secure message..."
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  className="flex-1 py-2 px-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent"
                  disabled={loading}
                />
                <button
                  type="submit"
                  disabled={loading || !newMessage.trim()}
                  className="px-4 py-2 rounded-lg bg-gradient-to-r from-pink-400 to-blue-400 text-white font-semibold flex items-center justify-center disabled:opacity-50"
                >
                  <Send className="h-4 w-4" />
                </button>
              </form>

              <div className="flex items-center justify-between text-xs text-gray-500 space-x-4">
                <div className="flex items-center space-x-1">
                  <Timer className="h-3 w-3" />
                  <select
                    value={selfDestructTime}
                    onChange={(e) => setSelfDestructTime(Number(e.target.value))}
                    className="text-xs bg-white border border-gray-300 rounded px-1"
                  >
                    <option value={60}>1 min (default)</option>
                    <option value={300}>5 min</option>
                    <option value={600}>10 min</option>
                    <option value={3600}>1 hour</option>
                    <option value={0}>No self-destruct</option>
                  </select>
                </div>
                <label className="flex items-center space-x-1">
                  <input type="checkbox" checked={readOnce} onChange={(e) => setReadOnce(e.target.checked)} />
                  <Eye className="h-3 w-3" />
                  <span>Read once</span>
                </label>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-400 text-center">
            <Shield className="h-16 w-16 mx-auto mb-4" />
            <h1>Select a user to start chatting</h1>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chat;
