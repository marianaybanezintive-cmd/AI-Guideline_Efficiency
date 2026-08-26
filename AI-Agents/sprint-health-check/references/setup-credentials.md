# Configuración de credenciales de Jira (una sola vez)

El agente necesita leer **changelog, story points y subtareas** de Jira. Eso requiere un
**API token personal** tuyo. No va en GitHub ni en el chat.

Token: https://id.atlassian.com/manage-profile/security/api-tokens

## ¿Dónde ejecutar el script?

En la **terminal integrada de Cursor**:

1. Abrí Cursor con el repo `AI-Guideline` como workspace
2. Presioná **Ctrl+`** (o menú *Terminal → New Terminal*)
3. Asegurate de estar en la raíz del repo (donde está `README.md`)
4. Ejecutá:

```powershell
powershell -ExecutionPolicy Bypass -File "AI-Agents/sprint-health-check/scripts/set_credentials.ps1"
```

También podés usar **Windows Terminal** o PowerShell desde el menú Inicio — el efecto
es el mismo: guarda las variables en tu perfil de Windows para que Python las encuentre.

## ¿Para qué sirve?

| Sin token | Con token |
|-----------|-----------|
| El agente no puede conectarse a Jira | Descarga los 130+ tickets del sprint con historial completo |
| 5 secciones del informe quedan vacías | Informe completo: estancados, alcance, QA aging, burndown, etc. |
| Hay que pegar el token en cada chat (inseguro) | Se configura **una vez** y persiste en tu máquina |

## Por qué REST y no el MCP de Jira

El MCP disponible no devuelve changelog, story points ni relación padre/subtarea, y sus
herramientas basadas en JQL fallan contra el endpoint `/rest/api/3/search` retirado por
Atlassian. Sin changelog no se pueden calcular 5 de las secciones del informe.
Ver [mcp-fallback.md](mcp-fallback.md) para el modo degradado.
