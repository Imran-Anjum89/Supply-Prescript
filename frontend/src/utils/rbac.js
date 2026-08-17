// Role-Based Access Control (RBAC) Permissions Engine

export const ROLE_PERMISSIONS = {
  "Supply Chain Planner": ["/", "/shipments", "/recommendations", "/profile"],
  "Risk Analyst": ["/", "/predictions", "/analytics", "/profile"],
  "Logistics Manager": ["/", "/recommendations", "/history", "/feedback", "/profile"],
  "System Administrator": ["/", "/shipments", "/predictions", "/recommendations", "/analytics", "/history", "/feedback", "/profile"],
};

export const normalizeRole = (roleStr) => {
  if (!roleStr) return "System Administrator";
  const lower = roleStr.toLowerCase();
  if (lower.includes("planner")) return "Supply Chain Planner";
  if (lower.includes("analyst")) return "Risk Analyst";
  if (lower.includes("manager") || lower.includes("logistics")) return "Logistics Manager";
  if (lower.includes("admin") || lower.includes("system") || lower.includes("director")) return "System Administrator";
  return roleStr;
};

export const canAccessPath = (userRole, path) => {
  const role = normalizeRole(userRole);
  const allowedPaths = ROLE_PERMISSIONS[role] || ROLE_PERMISSIONS["System Administrator"];
  return allowedPaths.includes(path);
};
