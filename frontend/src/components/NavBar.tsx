import { Link, useLocation, useNavigate } from "react-router-dom";
import { clearToken, getToken } from "../lib/auth";

const NavBar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const token = getToken();

  const handleLogout = () => {
    clearToken();
    navigate("/login");
  };

  const isAuthRoute = location.pathname === "/login" || location.pathname === "/register";

  return (
    <nav className="nav">
      <div className="nav-links">
        <Link to="/files">내 파일</Link>
        <Link to="/search">검색</Link>
      </div>
      <div className="nav-links">
        {token && !isAuthRoute ? (
          <button type="button" onClick={handleLogout}>
            로그아웃
          </button>
        ) : (
          <Link to="/login">로그인</Link>
        )}
      </div>
    </nav>
  );
};

export default NavBar;
