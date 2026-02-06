import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = "http://127.0.0.1:8001/api/blog/posts/";
const LOGIN_URL = "http://127.0.0.1:8001/api/login/";

function App() {
  const [posts, setPosts] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [images, setImages] = useState([]); // 'image' irraa gara 'images' (list)
  const [searchTerm, setSearchTerm] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);

  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => { fetchPosts(); }, []);

  const fetchPosts = async () => {
    setLoading(true);
    try {
      const response = await axios.get(API_URL);
      setPosts(response.data);
    } catch (error) { console.error("Error:", error); }
    finally { setLoading(false); }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(LOGIN_URL, { username, password });
      localStorage.setItem("token", response.data.token);
      setIsLoggedIn(true);
      setUsername(""); setPassword("");
      alert("Baga nagaan dhufte Admin!");
    } catch (error) { alert("Username ykn Password dogoggora!"); }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("title", title);
    formData.append("content", content);
    formData.append("author", 1);
    
    // Suuraalee baay'ee yoo filataman 'uploaded_images' keessa galchuuf
    if (images.length > 0) {
      for (let i = 0; i < images.length; i++) {
        formData.append("uploaded_images", images[i]);
      }
    }

    try {
      const config = { headers: { Authorization: `Token ${token}` } };
      if (editingId) {
        await axios.put(`${API_URL}${editingId}/`, formData, config);
        setEditingId(null);
      } else {
        await axios.post(API_URL, formData, config);
      }
      setTitle(""); setContent(""); setImages([]);
      fetchPosts();
    } catch (error) { alert("Rakkoon uumameera!"); }
  };

  const deletePost = async (id) => {
    const token = localStorage.getItem("token");
    if (window.confirm("Dhuguma balleessuu barbaadda?")) {
      try {
        await axios.delete(`${API_URL}${id}/`, {
          headers: { Authorization: `Token ${token}` }
        });
        fetchPosts();
      } catch (error) { alert("Permission hin qabdu!"); }
    }
  };

  const formatTime = (dateString) => {
    const options = { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const startEdit = (post) => {
    setEditingId(post.id);
    setTitle(post.title);
    setContent(post.content);
    window.scrollTo(0, 0);
  };

  const filteredPosts = posts.filter(p => 
    p.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    p.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div style={{ backgroundColor: '#0e1621', minHeight: '100vh', color: '#fff', padding: '20px', fontFamily: 'Segoe UI' }}>
      <div style={{ maxWidth: '500px', margin: '0 auto' }}>
        
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
          <h2 style={{ color: '#6ab3f3' }}>Waan-Ofii</h2>
          {isLoggedIn && <button onClick={handleLogout} style={{ background: '#e74c3c', color: '#fff', border: 'none', borderRadius: '5px', padding: '5px 10px', cursor: 'pointer' }}>Logout</button>}
        </div>

        {!isLoggedIn && (
          <form onSubmit={handleLogin} style={{ background: '#17212b', padding: '15px', borderRadius: '12px', marginBottom: '20px', border: '1px solid #2b5278' }}>
            <h4 style={{marginTop: 0}}>Admin Login</h4>
            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} style={{ width: '92%', padding: '10px', marginBottom: '10px', background: '#242f3d', border: 'none', color: '#fff', borderRadius: '8px' }} />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '92%', padding: '10px', marginBottom: '10px', background: '#242f3d', border: 'none', color: '#fff', borderRadius: '8px' }} />
            <button type="submit" style={{ width: '100%', background: '#5288c1', color: '#fff', border: 'none', padding: '10px', borderRadius: '8px', cursor: 'pointer' }}>Gali</button>
          </form>
        )}

        <input 
          type="text" placeholder="Barbaadi..." 
          value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)}
          style={{ width: '95%', padding: '12px', marginBottom: '20px', background: '#17212b', border: '1px solid #5288c1', color: '#fff', borderRadius: '25px' }}
        />

        {isLoggedIn && (
          <form onSubmit={handleSubmit} style={{ background: '#17212b', padding: '15px', borderRadius: '12px', marginBottom: '20px' }}>
            <h4 style={{margin: '0 0 10px 0', color: '#5288c1'}}>{editingId ? "Sirreessi" : "Haaraa"}</h4>
            <input type="text" placeholder="Mata-duree" value={title} onChange={(e) => setTitle(e.target.value)} required style={{ width: '95%', padding: '10px', marginBottom: '10px', background: '#242f3d', border: 'none', color: '#fff', borderRadius: '8px' }} />
            <textarea placeholder="Yaada kee..." value={content} onChange={(e) => setContent(e.target.value)} required style={{ width: '95%', padding: '10px', height: '60px', background: '#242f3d', border: 'none', color: '#fff', borderRadius: '8px', resize: 'none' }} />
            <div style={{ marginTop: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <input type="file" multiple onChange={(e) => setImages([...e.target.files])} style={{fontSize: '11px'}} />
              <button type="submit" style={{ background: editingId ? '#e67e22' : '#5288c1', color: '#fff', border: 'none', padding: '8px 20px', borderRadius: '20px', cursor: 'pointer' }}>{editingId ? "UPDATE" : "POST"}</button>
            </div>
          </form>
        )}

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {loading ? ( <p style={{ textAlign: 'center' }}>Loading...</p> ) : (
            filteredPosts.map(post => (
              <div key={post.id} style={{ background: '#182533', padding: '12px', borderRadius: '15px', marginBottom: '15px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                   <h4 style={{ color: '#6ab3f3', margin: '0' }}>{post.title}</h4>
                   {isLoggedIn && (
                     <div>
                       <button onClick={() => startEdit(post)} style={{ background: 'none', border: 'none', cursor: 'pointer', marginRight: '8px' }}>✏️</button>
                       <button onClick={() => deletePost(post.id)} style={{ background: 'none', border: 'none', cursor: 'pointer' }}>🗑️</button>
                     </div>
                   )}
                </div>

                {/* IMAGE ALBUM GRID */}
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: post.images && post.images.length > 1 ? '1fr 1fr' : '1fr', 
                  gap: '8px', marginTop: '10px' 
                }}>
                  {post.images && post.images.map(img => (
                    <img key={img.id} src={img.image.startsWith('http') ? img.image : `http://127.0.0.1:8001${img.image}`} 
                      style={{ width: '100%', height: post.images.length > 1 ? '150px' : 'auto', objectFit: 'cover', borderRadius: '10px' }} alt="Album" />
                  ))}
                </div>

                <p style={{ fontSize: '15px', marginTop: '10px' }}>{post.content}</p>
                <div style={{ textAlign: 'right', fontSize: '11px', color: '#708499', marginTop: '8px' }}>
                  {formatTime(post.created_at)} ✓✓
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default App;