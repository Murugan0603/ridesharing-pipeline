
FROM node:18-alpine

WORKDIR /app

# Step 3: package.json copy பண்றோம்
COPY package.json .

# Step 4: Dependencies install பண்றோம்
RUN npm install

# Step 5: மத்த எல்லா files-ம் copy பண்றோம்
COPY . .

# Step 6: இந்த port open பண்றோம்
EXPOSE 3001

# Step 7: Service start பண்றோம்
CMD ["node", "index.js"]