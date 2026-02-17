import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";

import Simple_API_Call from "../features/phase_0/Simple_API_CALL";

function AppRoutes(){
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/phase0" replace />} />
            <Route path="/phase0" element={<Simple_API_Call/>} />
        </Routes>
    );
}

export default AppRoutes