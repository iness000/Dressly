import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-100 z-[100]">
      <div className=" mx-auto px-6 h-20 flex items-center justify-between">
        
        {/* LEFt */}
        <div className="flex items-center gap-8 flex-1">
          <Link to="/how-it-works" className="text-sm font-semibold text-gray-600 hover:text-pink-600 transition-all">
            How It Works
          </Link>
          <Link to="/about" className="text-sm font-semibold text-gray-600 hover:text-pink-600 transition-all">
            About
          </Link>
        </div>

        <Link to="/" className="flex-shrink-0 text-center group">
          <h1 className="text-4xl font-black tracking-tighter flex items-center justify-center">
            <span className="text-pink-600">Dres</span>
            <span className="text-orange-500">sly</span>
          </h1>
        </Link>

        {/* RIGHT*/}
        <div className="flex items-center justify-end gap-6 flex-1">
          <Link 
            to="/quiz" 
            className="text-sm font-bold text-gray-700 hover:text-pink-600 transition-colors"
          >
            Take Your Quiz
          </Link>
          
          <Link 
            to="/login" 
            className="bg-[#ff1b6b] hover:bg-[#d4145a] text-white px-8 py-2.5 rounded-full font-bold text-sm shadow-lg shadow-pink-200 transition-all transform hover:-translate-y-0.5 active:scale-95"
          >
            Sign In
          </Link>
        </div>
        
      </div>
    </nav>
  );
};

export default Navbar;