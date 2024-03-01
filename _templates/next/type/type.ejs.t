---
to: frontend/types/<%= name %>.ts
---
export type <%= Name %> = {
<% params.split(',').forEach(function(param) { %>
  <%= param %>: string;
<% }); %>
}