# 🚀 Próximos Pasos - BTC Collateral Monitor

## ✅ Lo que está completo

- [x] Arquitectura del sistema documentada
- [x] Código base implementado (core, db, bot, dashboard)
- [x] Scripts de polling y setup
- [x] Docker y Docker Compose configurados
- [x] Guía de deployment escrita
- [x] Tests de integración creados
- [x] Script de instalación de cron job

---

## 📋 Pasos para poner en producción

### 1. Configurar Variables de Entorno

```bash
cd /home/ovservant/projects/rsk-collateral-monitor
cp .env.example .env
nano .env
```

**Importante:** Verificar las direcciones de contratos de Money on Chain:
- Visitar: https://docs.moneyonchain.com/
- O consultar en: https://rootstock.blockscout.com/

### 2. Instalar Dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Inicializar Base de Datos

```bash
python scripts/setup_db.py
```

### 4. Configurar Telegram Bot

1. Abrir Telegram y buscar @BotFather
2. Enviar `/newbot`
3. Seguir instrucciones para crear el bot
4. Copiar el token y pegarlo en `.env` como `TELEGRAM_BOT_TOKEN`
5. Tu Telegram ID es el `TELEGRAM_ADMIN_ID` (puedes obtenerlo con bots como @userinfobot)

### 5. Ejecutar Tests de Integración

```bash
python tests/test_integration.py
```

**Debe mostrar:**
- ✅ Connected to RSK
- ✅ Contract initialization OK
- ✅ Ratio calculations correct
- ✅ RBTC price fetched

### 6. Probar Polling Manual

```bash
python scripts/poll_positions.py
```

Revisar logs en `data/poller.log`

### 7. Instalar Cron Job

```bash
chmod +x scripts/install_cron.sh
./scripts/install_cron.sh
```

Verificar: `crontab -l`

### 8. Iniciar Dashboard

```bash
streamlit run dashboard/app.py
```

Acceder: http://localhost:8501

---

## 🔧 Comandos Útiles

### Ver logs del poller
```bash
tail -f data/poller.log
```

### Ver logs de cron
```bash
tail -f data/cron.log
```

### Ver cron jobs instalados
```bash
crontab -l
```

### Reiniciar dashboard
```bash
pkill -f "streamlit run"
streamlit run dashboard/app.py &
```

### Probar conexión a RSK
```bash
python -c "from core.contract_reader import get_contract_reader; print(get_contract_reader().is_connected())"
```

---

## ⚠️ Puntos de Atención

### 1. Direcciones de Contratos
Las direcciones en `.env.example` son **placeholders**. Debes verificar las direcciones oficiales de Money on Chain en:
- Documentación oficial: https://docs.moneyonchain.com/
- Block explorer: https://rootstock.blockscout.com/

### 2. Precios
El sistema usa CoinGecko para obtener el precio de RBTC. Si la API falla, usa BTC como fallback. En producción, considerar usar un oracle descentralizado.

### 3. Liquidación
Los umbrales por defecto son:
- 🟡 WARNING: 180%
- 🔴 CRITICAL: 160%
- 💀 LIQUIDATION: 150%

**Verificar** el threshold de liquidación exacto de Money on Chain (puede variar).

### 4. Telegram Bot
El bot actualmente envía alerts al admin. Para multi-usuario, implementar:
- Query de usuarios por wallet en la DB
- Enviar alertas a cada usuario registrado

---

## 📊 Métricas de Éxito

- [ ] Polling corre cada 10 minutos sin errores
- [ ] Alerts llegan vía Telegram cuando ratio < 180%
- [ ] Dashboard muestra posiciones actualizadas
- [ ] Base de datos crece con snapshots históricos
- [ ] Tests de integración pasan (RSK connection OK)

---

## 🆘 Troubleshooting Común

### "Failed to connect to RSK node"
```bash
# Verificar conectividad
curl https://public-node.rsk.co

# Probar RPC alternativo
# Editar .env: RSK_RPC_URL=https://mycrypto.rsk.co
```

### "No positions found"
- Registrar wallet vía Telegram: `/register 0x...`
- Verificar que la wallet tenga posiciones en Money on Chain

### "Telegram bot no envía alerts"
- Verificar token en `.env`
- Checkear logs: `tail -f data/poller.log`
- Probar envío manual con bot de Telegram

### Dashboard no carga
```bash
# Verificar puerto
netstat -tlnp | grep 8501

# Matar proceso y reiniciar
pkill -f streamlit
streamlit run dashboard/app.py &
```

---

## 📞 Soporte

- Documentación: `docs/ARCHITECTURE.md`, `docs/DEPLOYMENT.md`
- Código: `/home/ovservant/projects/rsk-collateral-monitor/`
- Logs: `data/poller.log`, `data/cron.log`

---

**Creado:** 2026-04-27  
**Pipeline:** Multi-Agent Pipeline v3.0 (Opción A - Selectivo)  
**Tiempo total:** ~20 minutos
