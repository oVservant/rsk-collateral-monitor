# Multi-Usuario Roadmap

**Estado Actual:** Single-User (solo Matias)  
**Objetivo:** Multi-Usuario (servicio público para comunidad Rootstock)

---

## 📊 Análisis del Estado Actual

### ✅ Lo que YA está listo para Multi-Usuario

| Componente | Estado | Notas |
|------------|--------|-------|
| **Database Schema** | ✅ Ready | Tabla `users` con telegram_id, wallet, preferences |
| **Telegram Bot** | ✅ Ready | Comandos `/register`, `/status`, `/alerts` |
| **Bot Commands** | ✅ Ready | Start, register, help, status, thresholds |
| **Alert System** | ✅ Ready | Envia alerts por Telegram |
| **Position Tracking** | ✅ Ready | Múltiples posiciones por wallet |
| **Dashboard** | 🟡 Partial | Muestra todas las posiciones (sin filtrar por usuario) |

### ❌ Lo que FALTA para Multi-Usuario

| Componente | Estado | Qué falta |
|------------|--------|-----------|
| **User Authentication** | ❌ Missing | Validar que telegram_id == dueño de wallet |
| **Privacy/Isolation** | ❌ Missing | Usuarios no deberían ver otras wallets |
| **Rate Limiting** | ❌ Missing | Prevenir abuso del bot |
| **User Management** | ❌ Missing | Admin commands para gestionar usuarios |
| **Billing/Subscription** | ❌ Missing | Si se cobra, necesita sistema de pagos |
| **Public Dashboard** | ❌ Missing | Landing page pública |
| **Documentation Pública** | ❌ Missing | Guía para usuarios finales |
| **Scaling** | ❌ Missing | PostgreSQL en vez de SQLite |
| **Monitoring** | 🟡 Partial | Health checks básicos, falta métricas de negocio |

---

## 🎯 Escenarios de Uso

### Escenario 1: Gratis para la Comunidad (Open Source)

**Modelo:** Servicio gratuito, mantenido por la comunidad

**Requerimientos:**
- [ ] Documentación pública clara
- [ ] Bot público en Telegram (@RSKCollateralBot)
- [ ] Dashboard público (solo métricas agregadas, no wallets individuales)
- [ ] Rate limiting básico (prevenir abuso)
- [ ] Terms of Service básico
- [ ] Donations opcionales (Gitcoin, BTC, RBTC)

**Ventajas:**
- ✅ Adopción rápida en la comunidad
- ✅ Feedback constante
- ✅ Contribuciones de la comunidad
- ✅ Posicionamiento como herramienta estándar

**Desventajas:**
- ❌ Costos de infraestructura (VPS, RPC nodes)
- ❌ Mantenimiento sin incentivo económico
- ❌ Riesgo de abuso sin rate limiting estricto

### Escenario 2: Freemium (Gratis + Premium)

**Modelo:** Básico gratis, features avanzadas pagas

**Free Tier:**
- ✅ 1 wallet monitoreada
- ✅ Alerts básicas (warning, critical, liquidation)
- ✅ Dashboard básico
- ✅ Polling cada 10 minutos

**Premium Tier ($5-10/mes):**
- ✅ Múltiples wallets (5-10)
- ✅ Alerts personalizadas (thresholds custom)
- ✅ Polling más frecuente (cada 5 min)
- ✅ Dashboard avanzado con analytics
- ✅ Export de datos (CSV, JSON)
- ✅ Email alerts (además de Telegram)
- ✅ Priority support

**Requerimientos:**
- [ ] Sistema de suscripciones (Stripe, crypto payments)
- [ ] User authentication robusta
- [ ] Database migration a PostgreSQL
- [ ] Admin dashboard para gestión
- [ ] Billing system
- [ ] Terms of Service + Privacy Policy

### Escenario 3: Enterprise (Protocolos DeFi)

**Modelo:** B2B - Vender a protocolos como Money on Chain

**Cliente:** Money on Chain, DeFi protocols on RSK

**Features:**
- ✅ White-label (su branding)
- ✅ API privada para integrar en sus dashboards
- ✅ Webhooks para alerts (no solo Telegram)
- ✅ SLA garantizado (99.9% uptime)
- ✅ Custom thresholds por protocolo
- ✅ Reporting avanzado
- ✅ Dedicated support

**Precio:** $500-2000/mes por protocolo

**Requerimientos:**
- [ ] API REST pública
- [ ] Webhook system
- [ ] SLA monitoring
- [ ] Multi-tenant architecture
- [ ] Contrato de servicio
- [ ] Soporte enterprise

---

## 🚀 Roadmap Recomendado

### Fase 1: Open Source (2-4 semanas)

**Objetivo:** Lanzar como herramienta gratuita para la comunidad

**Tareas:**
1. [ ] **Privacy & Isolation**
   - Filtrar dashboard por telegram_id
   - Validar ownership de wallets
   - Rate limiting básico

2. [ ] **Public Bot**
   - Crear @RSKCollateralBot en Telegram
   - Comandos documentados
   - Terms of Service básico

3. [ ] **Documentation**
   - README para usuarios finales
   - FAQ
   - Tutorial de setup

4. [ ] **Infrastructure**
   - Migrar a PostgreSQL (escalabilidad)
   - Deploy en VPS público
   - Monitoring básico (Uptime, errors)

5. [ ] **Community**
   - Anunciar en Twitter/LinkedIn
   - Post en foro Rootstock
   - Discord/Telegram de soporte

**Timeline:** 2-4 semanas  
**Costo:** ~$20-50/mes (VPS, RPC node)

### Fase 2: Freemium (1-2 meses después)

**Objetivo:** Monetizar features avanzadas

**Tareas:**
1. [ ] **Billing System**
   - Stripe integration (fiat)
   - Crypto payments (BTC, RBTC, USDC)
   - Subscription management

2. [ ] **Premium Features**
   - Múltiples wallets
   - Custom thresholds
   - Advanced analytics
   - Export de datos

3. [ ] **User Management**
   - Admin dashboard
   - User analytics
   - Churn monitoring

4. [ ] **Marketing**
   - Landing page
   - Pricing page
   - Testimonials

**Timeline:** 1-2 meses  
**Revenue potencial:** $100-500/mes (10-50 usuarios premium)

### Fase 3: Enterprise (3-6 meses después)

**Objetivo:** Vender a protocolos DeFi

**Tareas:**
1. [ ] **API REST**
   - Documentación (OpenAPI/Swagger)
   - Authentication (API keys)
   - Rate limiting por tier

2. [ ] **Webhooks**
   - Configurable endpoints
   - Retry logic
   - Signing/verification

3. [ ] **Enterprise Features**
   - White-label
   - SLA monitoring
   - Dedicated support
   - Custom integrations

4. [ ] **Legal**
   - Terms of Service enterprise
   - SLA agreements
   - Data privacy compliance

**Timeline:** 3-6 meses  
**Revenue potencial:** $500-2000/mes por cliente (2-5 clientes)

---

## 💰 Estimación de Costos e Ingresos

### Costos Mensuales (Fase 1 - Open Source)

| Item | Costo | Notas |
|------|-------|-------|
| VPS (DigitalOcean/Linode) | $20-40 | 2-4GB RAM, 2 CPU |
| RSK RPC Node (self-hosted) | $0-50 | O usar public nodes (rate limited) |
| PostgreSQL (managed) | $0-15 | Supabase free tier o self-hosted |
| Domain + SSL | $2 | Nombrecheap + Let's Encrypt |
| **TOTAL** | **$22-107/mes** | Depende de infra |

### Ingresos Potenciales (Fase 2 - Freemium)

| Tier | Precio | Usuarios | MRR |
|------|--------|----------|-----|
| Free | $0 | 100 | $0 |
| Premium | $5/mes | 20 | $100 |
| Premium | $10/mes | 10 | $100 |
| **TOTAL** | | **130 usuarios** | **$200/mes** |

### Ingresos Potenciales (Fase 3 - Enterprise)

| Cliente | Precio | Cantidad | MRR |
|---------|--------|----------|-----|
| Money on Chain | $1000/mes | 1 | $1000 |
| Otro protocolo | $500/mes | 2 | $1000 |
| **TOTAL** | | **3 clientes** | **$2000/mes** |

---

## 🏗️ Cambios Técnicos Necesarios

### 1. Database Migration (SQLite → PostgreSQL)

**Por qué:** SQLite no escala para múltiples usuarios concurrentes

**Cambios:**
```sql
-- PostgreSQL schema (similar pero con tipos nativos)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id TEXT UNIQUE NOT NULL,
    telegram_username TEXT,
    wallet_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    notification_preferences JSONB DEFAULT '{"warning": true, "critical": true}'
);

-- Índices para performance
CREATE INDEX idx_users_telegram ON users(telegram_id);
CREATE INDEX idx_users_wallet ON users(wallet_address);
```

**Migration script:** `scripts/migrate_to_postgres.py`

### 2. User Authentication

**Problema:** ¿Cómo validar que el usuario es dueño de la wallet?

**Solución 1: Message Signing**
```python
# Bot envía mensaje para firmar
message = "Sign this to verify ownership: {nonce}"
# Usuario firma con wallet
signature = web3.eth.sign(wallet, message)
# Bot verifica firma
signer = web3.eth.account.recover_message(message, signature)
if signer == wallet:
    # Ownership verified
```

**Solución 2: Small Transaction**
```python
# Bot pide enviar transacción mínima (0.0001 RBTC)
# Con memo único en tx
# Bot detecta tx y verifica ownership
```

**Recomendación:** Message signing (más simple, no gas fees)

### 3. Privacy & Isolation

**Cambios en queries:**
```python
# ANTES (muestra todo)
positions = db.get_all_positions()

# DESPUÉS (filtra por usuario)
positions = db.get_positions_by_telegram_id(telegram_id)
```

**Dashboard:**
- Filtrar por telegram_id
- Mostrar solo wallets del usuario
- Ocultar datos sensibles de otros usuarios

### 4. Rate Limiting

**Implementación:**
```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int, window_minutes: int):
        self.max_requests = max_requests
        self.window = timedelta(minutes=window_minutes)
        self.requests = {}
    
    def is_allowed(self, user_id: str) -> bool:
        now = datetime.now()
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Clean old requests
        self.requests[user_id] = [
            req for req in self.requests[user_id]
            if now - req < self.window
        ]
        
        # Check limit
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # Add request
        self.requests[user_id].append(now)
        return True

# Usage
limiter = RateLimiter(max_requests=10, window_minutes=1)
if not limiter.is_allowed(telegram_id):
    await bot.send_message("Rate limit exceeded. Try again in 1 minute.")
```

### 5. Admin Commands

**Nuevos comandos:**
```python
# Solo para admin (Matias)
/admin_stats - Ver estadísticas del sistema
/admin_users - Listar usuarios activos
/admin_broadcast - Enviar mensaje a todos los usuarios
/admin_suspend <user> - Suspender usuario
/admin_resume <user> - Reactivar usuario
```

---

## 📋 Checklist para Lanzamiento Público (Fase 1)

### Legal & Terms
- [ ] Terms of Service (básico)
- [ ] Privacy Policy
- [ ] Disclaimer (no financial advice)
- [ ] Contact info para soporte

### Technical
- [ ] Migrar a PostgreSQL
- [ ] User authentication (message signing)
- [ ] Privacy filters en dashboard
- [ ] Rate limiting implementado
- [ ] Error handling robusto
- [ ] Logging de errores
- [ ] Backup automático
- [ ] Monitoring (Uptime, errors)

### Documentation
- [ ] README para usuarios finales
- [ ] FAQ (preguntas frecuentes)
- [ ] Tutorial de uso del bot
- [ ] Guide de thresholds recomendados
- [ ] Troubleshooting básico

### Infrastructure
- [ ] Deploy en VPS público
- [ ] Domain configurado (ej: rskcollateral.com)
- [ ] SSL certificate
- [ ] PostgreSQL running
- [ ] Backup configurado
- [ ] Monitoring configurado

### Bot & UX
- [ ] Bot público (@RSKCollateralBot)
- [ ] Comandos documentados
- [ ] Welcome message claro
- [ ] Help command completo
- [ ] Error messages amigables

### Marketing & Community
- [ ] Landing page simple
- [ ] Twitter/LinkedIn announcement
- [ ] Post en foro Rootstock
- [ ] Discord/Telegram de soporte
- [ ] Demo video (opcional)

---

## 🎯 Recomendación Personal

**Mi recomendación:** Empezar con **Fase 1 (Open Source)**

**Por qué:**
1. ✅ **Validación rápida:** Ver si la comunidad lo usa
2. ✅ **Feedback:** Mejorar con input real de usuarios
3. ✅ **Reputación:** Posicionarte como contributor en RSK
4. ✅ **Bajo riesgo:** Sin compromiso de monetización
5. ✅ **Escalable:** Podés agregar premium después

**Timeline sugerido:**
- **Semana 1-2:** Implementar privacy + auth + rate limiting
- **Semana 3:** Deploy en VPS público + docs
- **Semana 4:** Lanzamiento en comunidad RSK

**Después de 1-2 meses:**
- Si hay adopción (>50 usuarios activos) → Considerar Fase 2 (Freemium)
- Si hay interés de protocolos → Considerar Fase 3 (Enterprise)

---

## 💡 Ideas Adicionales

### Features que Diferencian

1. **Multi-Protocol Support**
   - No solo Money on Chain
   - Agregar otros protocolos DeFi en RSK
   - Convertirse en "Collateral Monitor para todo RSK"

2. **Analytics Dashboard**
   - Gráficos de histórico de ratios
   - Comparativa con otros usuarios (anónimo)
   - Alertas de tendencias (ratio bajando consistentemente)

3. **Educational Content**
   - Explicar qué es collateral ratio
   - Cómo evitar liquidaciones
   - Mejores prácticas de DeFi

4. **Integration Partnerships**
   - Money on Chain oficial
   - Rootstock Foundation
   - Wallets populares (Ledger, Trezor)

5. **Gamification**
   - Badges por "sobrevivir" a caídas de mercado
   - Leaderboard de usuarios más conservadores
   - Achievements por tiempo sin liquidaciones

---

## 📞 Próximos Pasos Inmediatos

### Si querés lanzar como Open Source:

1. **Esta semana:**
   - [ ] Implementar privacy filters
   - [ ] Agregar message signing auth
   - [ ] Rate limiting básico
   - [ ] Migrar a PostgreSQL (opcional, pero recomendado)

2. **Próxima semana:**
   - [ ] Escribir docs para usuarios
   - [ ] Crear bot público en Telegram
   - [ ] Deploy en VPS
   - [ ] Testing con 2-3 usuarios beta

3. **Semana 3-4:**
   - [ ] Landing page simple
   - [ ] Anunciar en comunidad
   - [ ] Recolectar feedback
   - [ ] Iterar rápido

### Si preferís mantenerlo privado:

- [ ] Documentar cómo escalar a multi-usuario (ya hecho en este doc)
- [ ] Mantener código limpio para futura expansión
- [ ] No hay urgencia de cambios

---

**Conclusión:** El repo está **80% listo** para multi-usuario. Faltan principalmente:
1. Privacy filters (2-3 días)
2. User authentication (1-2 días)
3. Rate limiting (1 día)
4. PostgreSQL migration (2-3 días)
5. Documentation pública (2-3 días)

**Total:** 1-2 semanas de trabajo para tener Fase 1 lista.

---

**Tags:** #multiuser #saas #opensource #rootstock #defi #product
