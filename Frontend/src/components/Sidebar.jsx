import '../styles/sidebar.css';
import { Link, useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation();
  const currentPage = location.pathname.split("/")[1];
  console.log(currentPage);
  const menuItems = [
    { id: '', label: 'Learn', icon: 'fa-solid fa-file' },
    { id: 'practice', label: 'Practice', icon: 'fa-solid fa-brain' },
    { id: 'agent', label: 'Voice Agent', icon: 'fa-solid fa-voicemail' }
  ];

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h3>Roadmap</h3>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <Link
            key={item.id}
            className={`sidebar-item ${currentPage === item.id ? 'active' : ''}`}
            to={`/${item.id}`}
          >
            <i className={`sidebar-icon ${item.icon} ${currentPage === item.id ? 'active' : ''}`}></i>
            <span className={`sidebar-label ${currentPage === item.id ? 'active' : ''}`}>{item.label}</span>
          </Link>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;
